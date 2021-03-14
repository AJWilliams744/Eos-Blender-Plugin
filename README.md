# Eos Blender Plugin
Code for Blender plugin using Eos

Eos for python [click here](https://pypi.org/project/eos-py/)

I used info from [here](https://www.youtube.com/watch?v=JcHX4AT1vtg) to create the eyes

### Install Plugin
	Edit->Preferences->Add-ons->Install (Select "Eos_B_Plugin.py" from repo)
	Tick "Eos Interface" to enable or disable

### Loading Model
	Select file with model
	If additional blendshape file is needed select that too
	Click "Create New Model"

### Changing skin material
	Go to material properties
	Click the ball next to the material name
	Select either "ImageColourMat" or "VertexColourMat"
	
### Assign Image to Image Material
	Go to the shading tab
	Move boxes so they are inline / not overlapping
	Select the image texture node
	Select open image and choose correct image from files

### Deleting Eye Vertices
	Select the folder to store the .txt files of vertices
	Choose a file name, it will give a name if left blank
	Choose whether to overwrite the same named file or create a new one (if file exists name + "_X" will be added for you)
	Go into edit mode, use the face select tool to select faces in both eyes
	Go into object mode and click "Save Selected Vertices"
	Use the "Hide Vertex" button to hide or unhide vertices

	(You can select premade files by typing in the filename and choosing the correct folder)

### Adding Eye
	Select the file "eye.blend" from the repository
	Click "Load Eye Model" button
	
### Linking Eyes to Shape Movements
	With "Hide Vertex" ticked go into edit mode
	Pick two vertices located on each side of the left eye
	Go to object mode and click "Link Left Eye Vertices"
	You will see the index of both vertices in the box below
	Repeat for right eye
	
### Correcting Eye Shape
	Use the position offsets to move each eye in the correct place
	Use the "Eye Scale Offset" to get the scale right

	(The right eye uses the scale of left eye incase selected vertices are not mirror vertices)

### Randomising Expressions
	Each slider controls the standard deviation of a gaussian random distribution
	Choose desired SD for each and then click "Randomizes all the sliders"
	Leave it zero if you don't want it to randomize that value

### Resetting Sliders
	Click "Resets all the sliders to zero" button

### Changing Sliders
	Max shown is 20 until the show more button pressed
	Adjust sliders as you want

### Changing Eye Colour
	Go to the Shading Tab
	Select the eye and select "iris" material
	There is a "Hue Saturation Value" node connected to an "RGB Curves" just before an "Overlay" connected to the BSDF
	Change either the "Hue Saturation Value" or the "RBG Curves" to get the colour you want
	
	(Each eye has an indivudual material so any changes are per eye)

### Rendering Tips
	If using Eevee and the eyes enable "Screen Space Reflection" in Scene and enable "Refraction" in "Screen Space Reflection"
	For best results render using cycles and enable denoising in the Scene tab
