# Image Converter GUI APP for Arduino led display ssd1306 128x64
## About Project
<table border="0">
 <tr>
    <td><b style="font-size:50px">About Project</b></td>
    <td><b style="font-size:50px"> Screenshots</b></td>
 </tr>
 <tr>
    <td>
    Application has been created in order to easy convert image into your ***Arduino*** project with ***oled displays***
    How does it work While you open .png and .jpg (others extensions in the future) image in app, the algorithm convert it to hexdeicmal array. Then it             returns full code, ready to copy and put into the Arduino IDE. You can also preview how image will you like on your dislplay<br>
    </td>
    <td>
      <img src="https://user-images.githubusercontent.com/123249470/232137289-ff2707a7-a4bf-4e55-88a5-a469f54c3c3d.gif" width="420" height="350">
</p></td>
 </tr>
</table>

## How to connect display to Arduino
<p align="center">
<img src="https://user-images.githubusercontent.com/123249470/233432819-97b593ab-d380-4945-85ab-543dbb49921b.png" width="620" height="480">
</p>
IMPORTANT: If you have Arduino board with inputs SCK and SDA, use them instead of A4 and A5 inputs

## How to Contribute
1. Fork the Project
2. Clone repo with your GitHub username instead of ```YOUR-USERNAME```:<br>
```
$ git clone https://github.com/YOUR-USERNAME/Spoon-Knife 
```
3. Create new branch:<br>
```
git branch BRANCH-NAME 
git checkout BRANCH-NAME
```
4. Make changes and test<br>
5. Submit Pull Request with comprehensive description of change

## Task list
* upgrade graphics and style
* add more functions 
- add more than one display size
- make icon of the app
* show preview of an image 
- make app as .exe
* reverse color of image
- create function which generate full arduino code(not only arduino array) and connect it to switch button
## What I have learned
*	tkinter library skills 
*	basics of UX and GUI
*	image processing 
## Used libraries
* tkinter 
* customtkinter
* openCV
* numpy
## Version
Version 1.0
## License 
[MIT license](LICENSE)
