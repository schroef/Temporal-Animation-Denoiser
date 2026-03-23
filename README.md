# Temporal Animation Denoiser

This addon makes use of Blender's build Temporal Animation denoiser. Normally this only works when you have just rendered your scene. Using a code snippet found in [this article](https://artisticrender.com/how-to-denoise-an-animation-in-blender-using-temporal-denoising/) i converted it to a simple addon. The addon adds an extra panel under Samples in Render Properties

When ready to render your animation. Got to Render Properties panel > Sampling > Temporal Animation Denoiser. First set the output path for the animation, we are going to EXR files here. Then click "Setup Temporal", this will make sure we're using EXR Multi-Layer image and use the correct passes. Hit render and wait for it to finish.

Then go to "Denoise Render" and set the input path, this is the path we used for the render output path prior. Then choose an output path for the denoised images and hit "Denoise Temporal". Its best to have a console window open prior to this. This way you can keep track of the frames which have been denoised. THere is not visual feedback in the UI and Blender seems to be freezing.

!['Look UI'](https://raw.githubusercontent.com/wiki/schroef/temporal-animation-denoiser/images/temporal-animation-denoiser-v002.jpg?v20260323)

> Preview of the panel

BlenderShouthern SHotty made a nice video explaing this more into depth. 
![https://raw.githubusercontent.com/wiki/schroef/temporal-animation-denoiser/images/shouternshotty-720.jpg?v20260323](https://www.youtube.com/watch?v=NsR0UybO-PY)

Here is also another explanation by Robine Squares
![https://raw.githubusercontent.com/wiki/schroef/temporal-animation-denoiser/images/robinsquares-720.jpg?v20260323](https://youtu.be/yAbuPpbbATA?t=524)

### System Requirements

| **OS** | **Blender** |
| ------------- | ------------- |
| OSX | Blender 2.90+ |
| Windows | Blender 2.90+ |
| Linux | Not Tested |


### Installation Process

1. Download the latest <b>[release](https://github.com/schroef/temporal-animation-denoiser/releases/)</b>
2. If you downloaded the zip file.
3. Open Blender.
4. Go to File -> User Preferences -> Addons.
5. At the bottom of the window, choose *Install From File*.
6. Select the file `temporal-animation-denoiser-master.zip` from your download location..
7. Activate the checkbox for the plugin that you will now find in the list.
8. Set custom pie menu items by setting shortcuts for WM menu


### Changelog
[Full Changelog](CHANGELOG.md)





<!--
- Fill in data
 -
 -
-->

