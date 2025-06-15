#include <windows.h>

#include <chrono>
#include <codecvt>
#include <fstream>
#include <iostream>
#include <vector>

struct MouseData {
    long long int windowTitle;
    std::string state;
    long long int timeDiff;
    int dayTime;
    long xPos;
    long yPos;

    MouseData(long long int windowTitle, std::string state, long long int timeDiff, int dayTime, long xPos, long yPos)
        : windowTitle(windowTitle),
          state(std::move(state)),
          timeDiff(timeDiff),
          dayTime(dayTime),
          xPos(xPos),
          yPos(yPos) {}
};

long long int hashTitle(const std::string &title) {
    long long hash = 0;
    for (char i : title) {
        hash = (hash * 256 + i) % (1LL << 32);
    }
    return hash;
}

long long int prevTime;
std::pair<long, long> prevPos = {0, 0};
std::vector<MouseData> mouseData;

auto currentDateTimeMillis() {
    return std::chrono::duration_cast<std::chrono::milliseconds>(
               std::chrono::system_clock::now().time_since_epoch())
        .count();
}

auto dayTimeBroad() {
    time_t now = time(nullptr);
    struct tm *local_time = localtime(&now);
    auto hour = local_time->tm_hour;
    auto minute = local_time->tm_min;
    return (hour * 60 + minute) / 5;
}

void writeToFile() {
    CreateDirectory("C:\\mouse-data", nullptr);
    time_t now = time(nullptr);
    struct tm *local_time = localtime(&now);
    std::string date = std::to_string(local_time->tm_year + 1900) + "-" + std::to_string(local_time->tm_mon + 1) + "-" +
                       std::to_string(local_time->tm_mday);
    auto hour = local_time->tm_hour;
    auto minute = (local_time->tm_min) / 5;
    std::string fileName = "C:\\mouse-data\\" + date + "_" + std::to_string(hour) + "_" + std::to_string(minute) + ".csv";
    std::ifstream fileRead(fileName);
    // Append if file is not empty
    std::ofstream file;
    if (fileRead.peek() == std::ifstream::traits_type::eof()) {
        fileRead.close();
        file.open(fileName);
        file << "Window Title,State,Time Diff,Day Time,X Pos,Y Pos\n";
    } else {
        file.open(fileName, std::ios_base::app);
    }
    for (const auto &data : mouseData) {
        file << data.windowTitle << "," << data.state << "," << data.timeDiff << "," << data.dayTime << ","
             << data.xPos << "," << data.yPos << "\n";
    }
    file.close();
}

std::string getWindowName(HWND hwnd) {
    if (hwnd == nullptr) {
        return "";
    }
    int length = GetWindowTextLength(hwnd);
    if (length == 0) {
        return "";
    }
    std::vector<char> buffer(length + 1);
    int charsCopied = GetWindowTextA(hwnd, &buffer[0], length + 1);
    if (charsCopied == 0) {
        return "";
    }
    return std::string(buffer.data(), charsCopied);
}

HHOOK hMouseHook;

LRESULT CALLBACK LowLevelMouseProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION) {
        auto *pMouseStruct = (MSLLHOOKSTRUCT *)lParam;
        if (pMouseStruct != nullptr) {
            auto xPos = pMouseStruct->pt.x;
            auto yPos = pMouseStruct->pt.y;
            HWND hwnd = WindowFromPoint(pMouseStruct->pt);
            auto windowTitleStr = getWindowName(hwnd);
            if (windowTitleStr.empty()) return CallNextHookEx(hMouseHook, nCode, wParam, lParam);
            auto windowTitle = hashTitle(windowTitleStr);
            auto currentTime = currentDateTimeMillis();
            auto timeDiff = currentTime - prevTime;
            std::string state;

            switch (wParam) {
                case WM_MOUSEMOVE:
                    if (prevPos.first == xPos && prevPos.second == yPos) {
                        state = "NM";
                    } else if (prevPos.first == xPos) {
                        state = "VM";
                    } else if (prevPos.second == yPos) {
                        state = "HM";
                    } else {
                        state = "DM";
                    }
                    prevPos = {xPos, yPos};
                    break;
                case WM_LBUTTONDOWN:
                    state = "LD";
                    break;
                case WM_LBUTTONUP:
                    state = "LU";
                    break;
                case WM_RBUTTONDOWN:
                    state = "RD";
                    break;
                case WM_RBUTTONUP:
                    state = "RU";
                    break;
                case WM_MOUSEWHEEL:
                    state = "MW";
                    break;
                default:
                    state = "UN";
                    break;
            }
            if (state == "NM" || state == "UN") return CallNextHookEx(hMouseHook, nCode, wParam, lParam);
            mouseData.push_back({windowTitle, state, timeDiff, dayTimeBroad(), xPos, yPos});
            if (mouseData.size() >= 100) {
                writeToFile();
                mouseData.clear();
            }
            prevTime = currentTime;
        }
    }
    return CallNextHookEx(hMouseHook, nCode, wParam, lParam);
}

void SetHook() {
    hMouseHook = SetWindowsHookEx(WH_MOUSE_LL, LowLevelMouseProc, nullptr, 0);
    if (hMouseHook == nullptr) {
        std::cerr << "Mouse hook failed!" << std::endl;
    }
}

void Unhook() {
    UnhookWindowsHookEx(hMouseHook);
}

int main() {
    SetHook();
    prevTime = currentDateTimeMillis();

    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    Unhook();
    return 0;
}
