import os

__version__ = "0.3.0"

def pose_predictor_model_location():
    """Returns the location of the 68 point face landmark predictor model."""
    return os.path.join(os.path.dirname(__file__), 'models', 'shape_predictor_68_face_landmarks.dat')

def pose_predictor_five_point_model_location():
    """Returns the location of the 5 point face landmark predictor model."""
    return os.path.join(os.path.dirname(__file__), 'models', 'shape_predictor_5_face_landmarks.dat')

def face_recognition_model_location():
    """Returns the location of the face recognition model."""
    return os.path.join(os.path.dirname(__file__), 'models', 'dlib_face_recognition_resnet_model_v1.dat')

def cnn_face_detector_model_location():
    """Returns the location of the CNN face detection model."""
    return os.path.join(os.path.dirname(__file__), 'models', 'mmod_human_face_detector.dat')