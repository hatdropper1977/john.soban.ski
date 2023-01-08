Title:  Connect your 8BitDo M30 Bluetooth Controller to RetroPie
Date: 2022-04-30 03:21
Author: john-sobanski
Category: HOWTO
Tags: Linux, Ubuntu, 8BitDo
Slug: m30-linux
Status: published

I purchased the new [8BitDo](https://www.8bitdo.com/) [M30](https://www.8bitdo.com/m30/) Bluetooth controller for my [System76](https://system76.com/) (Ubuntu) Laptop.   I connected the M30 to [RetroPie](https://retropie.org.uk/docs/8Bitdo-Controller/) and then noticed issues with button layout for certain Six (6) Button Sega Genesis games.

In this blog post I will walk us through how to connect the new controller to RetroPie, and then how to deploy a configuration file to properly map the buttons.

Once you deploy the configuration file, you can enjoy Street Fighter II, for example, in Six Button mode.

![Street Fighter]({filename}/images/M30_Linux/01_Street_Fighter.png)

## Emulation
RetroPie delivers a premier emulation experience to retro gamers.  I will briefly discuss emulation in the next paragraph.

> Note:  In order to have a tenuous relationship to the theme of Machine Learning I had [Jasper AI]({filename}/jasper-ai.md) write this section

Do you remember the first time you played a video game? The Nintendo Entertainment System (NES) and (later) Sega Genesis introduced me to the medium. Millions of gamers around the world still enjoy playing retro games on original hardware. But for those of us who don't have the time or money to track down consoles and games from decades ago, emulation provides a great alternative. 
Emulation imitates the behavior of one system with another. In the context of retro gaming, this refers to imitating the behavior of older game consoles and computers on modern hardware.  Emulation provides a way for retro gamers to keep playing the games they love.

> NOTE:  Only emulate games which you have a legal right to.  

## 8BitDo
8BitDo designs controllers for modern consoles that recreate the feel of classic controllers. 8BitDo offers premium, sturdy controllers that allow retro gamers to play their favorite games without having to track down old hardware.

The 8BitDo M30 copies the look and feel of the classic Sega Genesis Six (6) Button controller.  Sega released a Six button controller in 1993 to compete with Nintendo’s record smashing SNES. Gamers love the ergonomic design and extra buttons.

![M30 Controller]({filename}/images/M30_Linux/02_M30_Controller.png)

Six button games for the Sega genesis include Street Fighter II, Mortal Kombat, Virtua Fighter, Batman Forever and Ranger X. For the best gaming experience, these games require the use of all six buttons on the controller.

# Connect the Controller
To connect the controller, follow the printout instructions for Android devices.

- Press & hold **B & start** to turn on the controller, **LED 1** blinks
- Press & hold **pair** for 2 seconds to enter pairing mode, **LED 1** pauses for a second then starts to rotate again
- Go to your Android device’s Bluetooth setting, pair with **8BitDo M30 gamepad**. LED becomes solid upon successful connection
- The controller will auto-reconnect to your Android device with the press of start after paring

You will see the Bluetooth controller connect under the Bluetooth menu.

![Bluetooth Connection]({filename}/images/M30_Linux/03_Bluetooth_Connected.png)

# Map the Buttons
The RetroPie Config files follow a SNES Controller approach, with four buttons on the face and two up top.  

Through trial and Error, I managed to figure out how to map the SNES style button layout to the Sega Genesis layout, which presents all six buttons on the face of the controller.

I present to you the results of my scientific method.

![SNES to Genesis Map]({filename}/images/M30_Linux/04_Snes_Genesis.png)

Through further investigations, I identified the numbers associated with each button on the M30 controller.

![M30 Button Numbers]({filename}/images/M30_Linux/05_Button_Numbers.png)

The following config file captures the proper map.

```bash
# 8Bitdo M30                  - http://www.8bitdo.com/     - http://www.8bitdo.com/m30/
# Firmware v1.13              - http://support.8bitdo.com/ - http://download.8bitdo.com/Firmware/Controller/M30/M30_Firmware_V1.13.zip

input_driver = "udev"
input_device = "8Bitdo M30 GamePad"
input_device_display_name = "8Bitdo M30"

input_vendor_id = "11720"
input_product_id = "1617"

input_b_btn = "1"
input_y_btn = "0"
input_select_btn = "10"
input_start_btn = "11"
input_a_btn = "7"
input_x_btn = "4"
input_l_btn = "3"
input_r_btn = "6"
input_l2_btn = "8"
input_r2_btn = "9"
input_menu_toggle_btn = "2"

input_b_btn_label = "A"
input_y_btn_label = "B"
input_select_btn_label = "Select"
input_start_btn_label = "Start"
input_a_btn_label = "C"
input_x_btn_label = "X"
input_l_btn_label = "Y"
input_r_btn_label = "Z"
input_l2_btn_label = "L"
input_r2_btn_label = "R"
input_menu_toggle_btn_label = "Guide"


input_up_axis = "-1"
input_down_axis = "+1"
input_left_axis = "-0"
input_right_axis = "+0"

input_up_axis_label = "D-pad Up"
input_down_axis_label = "D-pad Down"
input_left_axis_label = "D-pad Left"
input_right_axis_label = "D-pad Right"

input_up_btn = "h0up"
input_down_btn = "h0down"
input_left_btn = "h0left"
input_right_btn = "h0right"

input_up_btn_label = "Dpad Up"
input_down_btn_label = "Dpad Down"
input_left_btn_label = "Dpad Left"
input_right_btn_label = "Dpad Right"
```

Place the file in the directory **/opt/retropie/configs/all/retroarch/autoconfig/8BitDo\ M30\ gamepad.cfg**.

After you start RetroPie, you may have to configure the Controller for the main menu.  Go through the GUI to configure the controller.

Once you configure the M30 for the Main Menu, you can select a Mega Drive game.

The Emulator will then load your 8BitDo M30 Configuration for the Mega Drive.

![M30 Connected]({filename}/images/M30_Linux/06_M30_Connected.png)

## Quick Menu
If RetroPie defaults to a three button controller, use the **Quick Menu** to force a six button controller configuration. 

First, press the **Guide Button**, which looks like the checkboard Vans sneakers worn by Jeff Spiccoli.

This button brings up the **Quick Menu**.

![Quick Menu]({filename}/images/M30_Linux/08_Quick_Menu.png)

Scroll down to the **Controls** selection.

![Controls Selection]({filename}/images/M30_Linux/09_Controls_Selection.png)

Select **Port 1 Controls**.

![Port 1 Controls]({filename}/images/M30_Linux/10_Port1_Controls.png)

Select **Device Type**.

![Device Type]({filename}/images/M30_Linux/11_Device_Type.png)

Select **MD Joypad 6 Button**.

![MD Joypad]({filename}/images/M30_Linux/12_Md_Joypad.png)

RetroPie now displays the correct controller.

![Correct Controller]({filename}/images/M30_Linux/13_Correct_Controller.png)

Press the **G Button** to escape the menu and start your game!

## Batman Forever 
I recommend **Batman Forever** for the Sega Genesis.  

![Batman Forever]({filename}/images/M30_Linux/07_Batman_Forever.png)

I play my copy in High Definition on my [Analogue SG](https://www.analogue.co/mega-sg).  You can buy a used [Batman Forever cart on ebay](https://www.ebay.com/sch/i.html?_nkw=batman+forever+genesis) (clean link, non-affiliate) for around ten bucks.

![Batman Forever!]({filename}/images/M30_Linux/15_Analogue_Sg.png)

Acclaim entertainment released the video game **Batman Forever**, based on the hit movie of the same name, in 1995.  Acclaim unleashed the game onto multiple consoles.  The Genesis, SNES, Gameboy, Game Gear and Sega CD each received a version.  

![Batman Forever!]({filename}/images/M30_Linux/14_Batman_Forever.png)

Acclaim used very expensive (at the time) motion capture technology to create photo-realistic sprites.  They overlaid the sprites on the Mortal Kombat engine and plopped the characters into a Metroidvania style open world/ exploratory level design.

![Batman Forever!]({filename}/images/M30_Linux/16_Wata_Batman.png)

Critics (and fans) hate the game, I consider it an underappreciated Gem, if not masterpiece!  I played countless hours of Mortal Kombat back in the 90s and love the idea of (1) Playing Batman and (2) Breaking out of the limited Mortal Kombat levels into a huge world with jumps and platforms.

Batman Forever uses the Sega Genesis six button controller, with Mortal Kombat style high attacks, low attacks and a block button.  Batman Forever also includes a button for the Bat Grapple Gun.

# Conclusion
RetroPie stands in first place on the leaderboard of emulator platforms.  RetroPie turns Raspberry Pi into a retro game console. RetroPie comes pre-loaded with many popular emulators, and provides a simple interface for gamers to add more. RetroPie developers created a great interface for gamers to navigate and play games with ease. RetroPie provides the option to add custom buttons to the controller for specific functions (e.g. rewind the game, save states).

Emulation keeps the retro gaming hobby alive. Emulation provides a way for gamers to play their favorite games on modern hardware, which ensures that gamers will not forget these classics. It also allows new gamers to discover and enjoy seminal games. 

Let me know in the comments below if you have had success (or failure) with connecting your 8BitDo M30 controller to your RetroPie system.
