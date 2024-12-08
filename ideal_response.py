import cv2
import numpy as np
import pyartoolkit

# Initialize ARToolKit
artoolkit = pyartoolkit.ARToolKit()

# Load marker pattern
marker_pattern = pyartoolkit.MarkerPattern("patt.hiro")

# Set camera parameters
camera_params = np.array([
    [640, 0, 320],
    [0, 640, 240],
    [0, 0, 1]
])

# Open video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect markers in frame
    markers, ids, rejected = artoolkit.detect_markers(gray, camera_params, marker_pattern)
    
    # Draw marker boundaries on frame
    for marker in markers:
        cv2.polylines(frame, [marker.contour], True, (0, 255, 0), 2)
        cv2.putText(frame, str(marker.id), tuple(marker.center), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    # Overlay digital content on markers
    for marker in markers:
        if marker.id == 0:
            # Load 3D model
            model = pyartoolkit.load_model("teapot.wrl")
            
            # Render 3D model on marker
            model.render(frame, marker.pose, camera_params)
            
    # Display frame
    cv2.imshow("AR Demo", frame)
    
    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()