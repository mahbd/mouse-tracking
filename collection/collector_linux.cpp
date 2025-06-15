#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <utility>
#include <chrono>
#include <ctime>
#include <cstring>
#include <libinput.h>
#include <libudev.h>
#include <fcntl.h>
#include <unistd.h>
#include <poll.h>
#include <sys/stat.h>

struct MouseData
{
    long long int windowTitle; // Will be 0 (Unknown) on Wayland
    std::string state;
    long long int timeDiff;
    int dayTime;
    long xPos; // Accumulated X (relative)
    long yPos; // Accumulated Y (relative)

    MouseData(long long int windowTitle, std::string state, long long int timeDiff, int dayTime, long xPos, long yPos)
        : windowTitle(windowTitle),
          state(std::move(state)),
          timeDiff(timeDiff),
          dayTime(dayTime),
          xPos(xPos),
          yPos(yPos) {}
};

// No need for hashTitle if we can't get titles
long long int prevTime;
std::pair<long, long> currentPos = {0, 0}; // Use this to accumulate deltas
std::vector<MouseData> mouseData;

auto currentDateTimeMillis()
{
    return std::chrono::duration_cast<std::chrono::milliseconds>(
               std::chrono::system_clock::now().time_since_epoch())
        .count();
}

auto dayTimeBroad()
{
    time_t now = time(nullptr);
    struct tm *local_time = localtime(&now);
    auto hour = local_time->tm_hour;
    auto minute = local_time->tm_min;
    return (hour * 60 + minute) / 5;
}
// --- End portable parts ---

// --- Linux specific file writing ---
void writeToFile()
{
    const char *homeDir = getenv("SUDO_USER") ? getenv("SUDO_USER") : getenv("USER");
    std::string homePath;

    if (homeDir)
    {
        homePath = "/home/" + std::string(homeDir);
    }
    else
    {
        std::cerr << "Cannot determine user's HOME directory when running as root. Using /root." << std::endl;
        homePath = "/home/mah";
    }

    std::string dataDir = homePath + "/mouse-data";

    // Create directory if it doesn't exist (mode 0755)
    mkdir(dataDir.c_str(), 0755);

    time_t now = time(nullptr);
    struct tm *local_time = localtime(&now);
    std::string date = std::to_string(local_time->tm_year + 1900) + "-" + std::to_string(local_time->tm_mon + 1) + "-" +
                       std::to_string(local_time->tm_mday);
    auto hour = local_time->tm_hour;
    auto minute = (local_time->tm_min) / 5;
    std::string fileName = dataDir + "/" + date + "_" + std::to_string(hour) + "_" + std::to_string(minute) + ".csv";

    std::ifstream fileRead(fileName);
    std::ofstream file;
    if (!fileRead.is_open() || fileRead.peek() == std::ifstream::traits_type::eof())
    {
        fileRead.close();
        file.open(fileName, std::ios_base::out);
        file << "WindowTitle,State,Time Diff,Day Time,X Pos,Y Pos\n";
    }
    else
    {
        fileRead.close();
        file.open(fileName, std::ios_base::app);
    }

    if (!file.is_open())
    {
        std::cerr << "Could not open file: " << fileName << std::endl;
        return;
    }

    for (const auto &data : mouseData)
    {
        file << data.windowTitle << "," << data.state << "," << data.timeDiff << "," << data.dayTime << ","
             << data.xPos << "," << data.yPos << "\n";
    }
    file.close();
    // Change ownership of the file to the Sudo user if possible
    if (getenv("SUDO_USER") && getenv("SUDO_UID") && getenv("SUDO_GID"))
    {
        chown(fileName.c_str(), std::stoi(getenv("SUDO_UID")), std::stoi(getenv("SUDO_GID")));
    }
}
// --- End file writing ---

// --- libinput specific parts ---
static int open_restricted(const char *path, int flags, void *user_data)
{
    // libinput needs to open devices, MUST run as root
    int fd = open(path, flags);
    return fd < 0 ? -1 : fd;
}

static void close_restricted(int fd, void *user_data)
{
    close(fd);
}

const static struct libinput_interface interface = {
    .open_restricted = open_restricted,
    .close_restricted = close_restricted,
};

void process_event(struct libinput_event *event)
{
    struct libinput_event_pointer *p;
    std::string state = "UN";
    double dx = 0, dy = 0, wheel_y = 0;
    bool is_move = false;

    enum libinput_event_type type = libinput_event_get_type(event);

    switch (type)
    {
    case LIBINPUT_EVENT_POINTER_MOTION:
        p = libinput_event_get_pointer_event(event);
        dx = libinput_event_pointer_get_dx(p);
        dy = libinput_event_pointer_get_dy(p);
        is_move = true;
        break;
    case LIBINPUT_EVENT_POINTER_BUTTON:
        p = libinput_event_get_pointer_event(event);
        {
            uint32_t button = libinput_event_pointer_get_button(p);
            enum libinput_button_state bstate = libinput_event_pointer_get_button_state(p);
            // Map BTN_LEFT/RIGHT (codes from input-event-codes.h)
            if (button == 272)
                state = (bstate == LIBINPUT_BUTTON_STATE_PRESSED) ? "LD" : "LU";
            else if (button == 273)
                state = (bstate == LIBINPUT_BUTTON_STATE_PRESSED) ? "RD" : "RU";
            else
                state = "UN"; // Ignore other buttons like middle click for now
        }
        break;
    case LIBINPUT_EVENT_POINTER_AXIS:
        p = libinput_event_get_pointer_event(event);
        // Check if it's a vertical scroll (usually)
        if (libinput_event_pointer_has_axis(p, LIBINPUT_POINTER_AXIS_SCROLL_VERTICAL))
        {
            wheel_y = libinput_event_pointer_get_axis_value(p, LIBINPUT_POINTER_AXIS_SCROLL_VERTICAL);
            if (wheel_y != 0)
            {
                state = "MW";
            }
        }
        break;
    default:
        return; // Ignore other event types (keyboard, touch, etc.)
    }

    long prevX = currentPos.first;
    long prevY = currentPos.second;

    // Update position if it was a move event
    if (is_move)
    {
        currentPos.first += static_cast<long>(dx);
        currentPos.second += static_cast<long>(dy);

        // Determine move type (DM, VM, HM, NM)
        if (dx != 0 && dy != 0)
            state = "DM";
        else if (dx == 0 && dy != 0)
            state = "VM";
        else if (dx != 0 && dy == 0)
            state = "HM";
        else
            state = "NM"; // Should not happen if is_move is true and dx/dy=0, but for safety.
    }

    if (state == "UN" || state == "NM")
    {
        return; // Only log actual moves or clicks/wheel
    }

    auto currentTime = currentDateTimeMillis();
    auto timeDiff = currentTime - prevTime;

    // We *CANNOT* get window title, use 0 as a placeholder
    long long int windowTitle = 0;

    mouseData.push_back({windowTitle, state, timeDiff, dayTimeBroad(), currentPos.first, currentPos.second});
    prevTime = currentTime;

    // Check buffer size
    if (mouseData.size() >= 100)
    {
        writeToFile();
        mouseData.clear();
    }
}

int main()
{
    struct libinput *li;
    struct udev *udev;

    // Check if running as root
    if (getuid() != 0)
    {
        std::cerr << "This program MUST be run as root (using sudo) on Wayland." << std::endl;
        return 1;
    }

    udev = udev_new();
    if (!udev)
    {
        std::cerr << "Failed to initialize udev" << std::endl;
        return 1;
    }

    li = libinput_udev_create_context(&interface, nullptr, udev);
    if (!li)
    {
        std::cerr << "Failed to initialize libinput context from udev" << std::endl;
        udev_unref(udev);
        return 1;
    }

    if (libinput_udev_assign_seat(li, "seat0") != 0)
    {
        std::cerr << "Failed to assign seat" << std::endl;
        libinput_unref(li);
        udev_unref(udev);
        return 1;
    }

    std::cout << "Starting Linux (Wayland/libinput) mouse logger... Run with sudo." << std::endl;
    std::cout << "WARNING: Window titles cannot be captured. Coordinates are accumulated." << std::endl;
    std::cout << "Press Ctrl+C to stop." << std::endl;

    prevTime = currentDateTimeMillis();
    struct libinput_event *event;
    struct pollfd fds;

    fds.fd = libinput_get_fd(li);
    fds.events = POLLIN;
    fds.revents = 0;

    libinput_dispatch(li); // Dispatch initial events

    while (poll(&fds, 1, -1) > -1)
    { // Poll indefinitely
        libinput_dispatch(li);
        while ((event = libinput_get_event(li)) != nullptr)
        {
            process_event(event);
            libinput_event_destroy(event);
            libinput_dispatch(li); // Dispatch after processing
        }
    }

    // Cleanup (won't be reached by Ctrl+C, needs signal handling for graceful exit)
    std::cerr << "Exiting..." << std::endl;
    if (!mouseData.empty())
    {
        writeToFile();
    }
    libinput_unref(li);
    udev_unref(udev);

    return 0;
}

// g++ collector_linux.cpp -o wayland_mouse_logger -linput -ludev -std=c++17