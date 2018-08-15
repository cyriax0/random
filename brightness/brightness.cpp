#include <iostream>
#include <fstream>
#include <string>
#include <regex>

#define BRIGHTNESS_DEVICE "/sys/class/backlight/intel_backlight/brightness"
#define MAX_BRIGHTNESS_DEVICE "/sys/class/backlight/intel_backlight/max_brightness"
using namespace std;

int getMaxBrightness(){
    int max_brightness;
    ifstream device;
    device.open(MAX_BRIGHTNESS_DEVICE);
    device >> max_brightness;
    device.close();
    return max_brightness;
}

int getBrightness(){
    int brightness;
    ifstream device;
    device.open(BRIGHTNESS_DEVICE);
    device >> brightness;
    device.close();
    return brightness;
}

void setBrightness(int raw_value){
    ofstream device;
    device.open(BRIGHTNESS_DEVICE);
    device << raw_value;
    device.close();
}



#define INPUT_SEPARATOR "(([+-]?)[[:digit:]]*)(%?)"

int main(int argc, char * argv[]){
    if (argc != 2){
        cout << "Usage:\n\tbrightness [+-][NUMBER]%\n\tbrightness get" << endl;
    } else if (argc == 2){
        string argument(argv[1]);
        if (argument == "get"){
            cout << (getBrightness()*100/getMaxBrightness()) << "%" << endl;
            return 0;
        }
        smatch match;
        regex expression(INPUT_SEPARATOR);
        if (regex_search(argument,match,expression)){
            int number = stoi(match[1]);
            bool absolute = (match[2] == "");
            bool percentage = (match[3] == "%");
            int max_brightness = getMaxBrightness();
            int target_brightness;
            if (percentage){
                if (absolute){
                    target_brightness = max_brightness*number/100;
                } else {
                    target_brightness = getBrightness() + max_brightness*number/100;
                }
            } else {
                if (absolute){
                    target_brightness = number;
                } else {
                    target_brightness = getBrightness() + number;
                }
            }
            if (target_brightness <= 0) target_brightness = 1;
            if (target_brightness > max_brightness) target_brightness = max_brightness;
            if (absolute && number == 0) target_brightness = 0;
            setBrightness(target_brightness);
        } else {
            cout << "Could not parse: "<< argument << endl;
        }
    }
    return 0;
}
