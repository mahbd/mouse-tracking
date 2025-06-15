#include <windows.h>
#include <chrono>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

long long int hashTitle(const std::string &title)
{
    long long hash = 0;
    for (char i : title)
    {
        hash = (hash * 256 + i) % (1LL << 32);
    }
    return hash;
}

long long int prevTime;
std::pair<long, long> prevPos = {0, 0};

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

std::string getWindowName(HWND hwnd)
{
    if (hwnd == nullptr)
        return "";
    int length = GetWindowTextLength(hwnd);
    if (length == 0)
        return "";
    std::vector<char> buffer(length + 1);
    GetWindowTextA(hwnd, &buffer[0], length + 1);
    return std::string(buffer.data());
}

HHOOK hMouseHook;

LRESULT CALLBACK LowLevelMouseProc(int nCode, WPARAM wParam, LPARAM lParam)
{
    if (nCode == HC_ACTION)
    {
        auto *pMouseStruct = (MSLLHOOKSTRUCT *)lParam;
        if (pMouseStruct != nullptr)
        {
            auto xPos = pMouseStruct->pt.x;
            auto yPos = pMouseStruct->pt.y;
            HWND hwnd = WindowFromPoint(pMouseStruct->pt);
            auto windowTitleStr = getWindowName(hwnd);

            if (windowTitleStr.empty())
                return CallNextHookEx(hMouseHook, nCode, wParam, lParam);

            auto windowTitle = hashTitle(windowTitleStr);
            auto currentTime = currentDateTimeMillis();
            auto timeDiff = currentTime - prevTime;
            std::string state;

            switch (wParam)
            {
            case WM_MOUSEMOVE:
                if (prevPos.first == xPos && prevPos.second == yPos)
                    state = "NM";
                else if (prevPos.first == xPos)
                    state = "VM";
                else if (prevPos.second == yPos)
                    state = "HM";
                else
                    state = "DM";
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

            if (state == "NM" || state == "UN")
                return CallNextHookEx(hMouseHook, nCode, wParam, lParam);

            std::cout << windowTitle << "," << state << "," << timeDiff << "," << dayTimeBroad() << ","
                      << xPos << "," << yPos << std::endl;

            prevTime = currentTime;
        }
    }
    return CallNextHookEx(hMouseHook, nCode, wParam, lParam);
}

void SetHook()
{
    hMouseHook = SetWindowsHookEx(WH_MOUSE_LL, LowLevelMouseProc, nullptr, 0);
    if (hMouseHook == nullptr)
    {
        std::cerr << "Mouse hook failed!" << std::endl;
    }
}

void Unhook() { UnhookWindowsHookEx(hMouseHook); }

int main()
{
    SetHook();
    prevTime = currentDateTimeMillis();
    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    Unhook();
    return 0;
}