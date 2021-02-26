# Eos Blender Plugin
Code for Blender plugin using Eos

INSTALL PLUGIN
	Edit->Prefrences->Add-ons->Install
	Tick Eos Interface to enable or disable

LOADING MODEL
	Select file with model
	If additional blendshape file is needed select that too
	Click "Create New Model"

DELETING EYE VERTICES
	Select the folder to store the txt files of vertices
	Choose a file name, it will give a name if left blank
	Choose whether to overwrite the same named file or create a new one (if file exists name + "_X" will be added for you)
	Go into edit mode, use the face select tool to select faces in both eyes
	Go into object mode and click "Save Selected Vertices"
	Use the "Hide Vertex" button to hide or unhide vertices

	(You can select premade files by typing in the filename and choosing the correct folder)

ADDING EYE
	Select the file "eye.blend" from the repository
	Click "Create Eye Model" button
	
LINKING EYES TO SHAPE MOVEMENTS
	With "Hide Vertex" ticked go into edit mode
	Pick two vertices located on each side of the left eye
	Go to object mode and click "Link Left Eye Vertices"
	You will see the index of both vertices in the box below
	Repeat for right eye
	
CORRECTING EYE SHAPE
	Use the position offsets to place each eye in the correct place
	Use the "Eye Scale Offset" to get the scale right

RANDOMIZING EXPRESSIONS
	Each slider controls the standard deviation a gaussian random distribution
	Choose desired SD for each and then click "Randomizes all the sliders"
	Leave it zero if you don't want it to randomize that value

RESETTING SLIDERS
	Click "Resets all the sliders to zero" button

CHANGING SLIDERS
	Max shown is 20 until the show more button pressed
	Adjust sliders as you want

CHANGING EYE COLOUR
	

RENDERING TIPS
	If using Eevee and the eyes enable "Screen Space Reflection" in Scene and enable "Refraction" in "Screen Space Reflection"
	For best results render using cycles and enable denoising in the Scene tab


