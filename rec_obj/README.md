## Installing OpenCV on Windows

-------------------------------
OpenCV is an open-source computer vision library that can be used to process and analyze images and videos in real-time. In this guide, we will walk you through the steps to install OpenCV on Windows.

### Installation Steps

1. Download the latest version of OpenCV for Windows from the official website - https://opencv.org/releases/.

2. Extract the downloaded file into a directory of your choice. For example, you can extract it to `C:\opencv`.

3. Add the OpenCV bin directory to your operating system PATH. Here's how:

   - Open the Start Menu and type "Environment Variables" and select the "Edit the system environment variables" option.
   - In the "System Properties" window, click "Environment Variables".
   - In the "System Variables" section, select the PATH variable and click "Edit".
   - Click "New" and add the path to the OpenCV bin folder, for example: `C:\opencv\build\x64\vc15\bin`.
   - Click OK in all open windows to confirm changes.

4. Verify that OpenCV is installed correctly by opening a command prompt and typing `python` to start the Python interpreter. Then, type the following command to import the OpenCV library:

   ```besh
   $ import cv2
   ```
    If you  don't get any error messages, OpenCV is installed correctly.

-------------------------------
## Running the Program

To run the program, follow these steps:

1. Put the positive and negative images in their respective folders. For example, put the positive images in `positive_imgs` and negative images in `negative_imgs`.

2. Create `annotations.txt` file:

    <!-- Run the following command on the terminal: -->
    ```besh
    $ python create_file_annotations.py
    ```
    This command will launch a GUI tool that you can use to select and annotate objects in the positive images. The tool will save the annotations in the `annotations.txt` file.

3. Create `bg.txt` file:

    <!-- Run the following command on the terminal: -->
    ```besh
    $ python create_file_bg.py
    ```
    This code creates a text file named `bg.txt` with the paths to the negative images that will be used to train the object detection classifier

4. Training a Cascade Classifier in OpenCV:

    <!-- Run the following command on the terminal: -->
    ```besh
    $ python train.py
    ```
    This code trains a cascade classifier in OpenCV, which is used for object detection in images. The script takes the following parameters:
    - `w` and `h`: width and height of the training images
    - `numPos`: number of positive samples
    - `numNeg`: number of negative samples
    - `numStages`: number of cascade stages
    - `path`: file to save the cascade in
-------------------------------
