# [The Bengaluru Mobility Challenge, 2024](https://ieee-dataport.org/competitions/bengaluru-mobility-challenge-2024)
## Team "KolKGP Convergence"
Participant in the Phase 1 of The Bengaluru Mobility Challenge <br/>
<br/>
Member: Pritish Saha
<br/>
<br/> More details about the event can be found here: [Link](https://dataforpublicgood.org.in/bengaluru-mobility-challenge-2024/)

### Problem Statement:
The participants in this phase will be provided with camera feeds from 23 Safe City cameras in northern Bengaluru, around the IISc campus. The task will be to provide short-term (e.g., 30 minutes into the future) predictions of the vehicle counts (by vehicle type) as well as vehicle turning patterns at certain points and junctions of the road network. The predictions may be at different points different from the locations where the camera feeds are available.



### Scripts and Files

#### `src`
This folder contains all the files needed to run the pipeline.
1. **`app.py`** : The main driver code that has to be run. Takes an input JSON file and output JSON file as CLI arguments that provide the video paths and the path to the final output counts. 

2. **`config.py`** : This file contains a dictionary of the co-ordinates of the turning pattern detection boxes required for each camera location/junction.

3. **`outputTemplate.py`** : Here, the output format required by the organisers is stored, which is again a dictionary of every turning pattern possible, for both counts and predictions, which is to be converted and submitted in JSON format.

4. **`customCounter.py`** : An *ultralytics* source code for creating a counter object that we modified based on our requirements.

5. **`video_processor.py`** : This file houses the *VideoProcessor* class that does the video processing to detect, track and count the turns made by the various classes of vehicles. 

6. **`forecasting.py`** : The *Forecaster* class is located here, which uses the count data collected while counting, to produce a prediction of the turn counts for the future. Preprocessing of the data logged onto the excel also takes place here.

7. **`output_handler.py`** : Just a simple script to process the derived outputs into the dictionary defined by *outputTemplate.py*.

Only `app.py` is supposed to be run, the other files cannot run on their own.\
Command to run: `python3 src/app.py data/input.json data/output.json`\
Format for `data/input.json`:
```
{
   "Cam_ID": 
    {
        "Vid_1": "path/to/your/video/Cam_ID_vid_1.mp4",
        "Vid_2": "path/to/your/video/Cam_ID_1_vid_2.mp4"
    }
}
```
The paths inside `input.json` should be relative to where you run the command from, or absolute paths.

#### `models`
- **`best.pt`** : The trained YOLOv8 model to detect the 7 classes of vehicles.

#### `scripts`
These are some other scripts used to ease the process of trainng and development but is not needed to run the framework.
1. **`extract_images.py`** : We used this script to extract images from the video downloaded from the dataset every *n* frames which we can set based on the number of images required.

2. **`auto_annotate.py`** : After making a basic model, we ran the extracted images through the model to annotate the images for us, and we would verify/edit the annotations. This script automated the annotation process and saved us a lot of time.

3. **`data_split.py`** : A simple script to split the images dataset into training, testing and validation sets.

4. **`stream.py`** : This code lets us view the YOLO model in action on a live video. It shows us the predictions being made in real-time in the video.

5. **`capture_coordinates.py`** : This script allowed us to simplify the process of creating the turn count boxes at the junctions. We simply opened the screenshot of the junction provided by the organisers and clicked on the corners of the box, and the pixel values are automatically logged.

6. **`view.py`** : Code that lets us view the turning boxes created against the actual images of the junction for easier interpretation. 

7. **`predict_arima.py`** : The script to test various forecasting models and methods using ARIMA, by tuning parameters, using different types of datasets etc.

8. **`data_combine.py`** : A simple script to combine the annotated image folders by all the team members.

#### `data`
- **`data.yaml`** : This file is used to specify dataset location during training, and holds the list of classes.

### `requirements.txt`
This file lists all the python dependencies. Install them using:
`pip3 install -r requirements.txt`

### Open-Source Material

**YOLOv8** by *Ultralyitcs* is an open source, real-time object detection and image segmentation model.

**labelimg** is an annotation tool that provides features to draw and edit bounding boxes in the format required by YOLOv8.

### Docker
A Dockerfile has been created to install necessary libraries including CUDA for the model to be able to use GPUs. The docker file can be built and run in a simple way.\
Build: `docker build -t username/imagename:version .`\
Push: `docker push  username/imagename:version`\
Run: `docker run --rm --gpus all -v 'YOUR_VIDEO_DIRECTORY_ON_HOST:/app/videos' -v 'YOUR_OUTPUT_DIRECTORY_ON_HOST:/app/output' username/imagename:version python3 src/app.py /app/videos/input.json /app/output/output.json`

The run command takes the input and output json file to read, process and save the results in.
- You need to place your `input.json` in `YOUR_VIDEO_DIRECTORY_ON_HOST`.
- The paths in `input.json` should be relative to `/app/videos/` inside the container (e.g., `"Vid_1": "/app/videos/Cam_ID_vid_1.mp4"`).
- The output will be saved in `YOUR_OUTPUT_DIRECTORY_ON_HOST`.

### System Requirements

- CPU - Core i5
- GPU - NVIDIA GTX 1650 with CUDA support
- RAM - 8 GB
- Disk Space - 10 GB
- Around 1GB of GPU memory would be used for realtime inference.

