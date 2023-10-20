#This code is implemented as part of CFC 2023 for Project Nutribuddy
#The purpose of the code is Plant health status prediction
from ultralytics import YOLO
import cv2
import time

#Assigning the custom trained ML model
model = YOLO('model.pt')

#pass plant image
img = cv2.imread('image.jpg')

# First run to 'warm-up' the model
model.predict(source=img, save=False, save_txt=False, conf=0.5, verbose=False)

# Second run
t_start = time.monotonic()
results = model.predict(source=img, save=False, save_txt=False, conf=0.5, verbose=False)
dt = time.monotonic() - t_start

# Show results
boxes = results[0].boxes
names = model.names
confidence, class_ids = boxes.conf, boxes.cls.int()
rects = boxes.xyxy.int()
for ind in range(boxes.shape[0]):
    print("Result", names[class_ids[ind].item()], confidence[ind].item(), rects[ind].tolist())


# Explainable AI Integration - Explain the prediction using LIME

explainer = lime_image.LimeImageExplainer()

def predict_wrapper(images):
    return model.predict(images, conf=0.5, verbose=False)

explainer_interpreter = lime_image.LimeImageInterpreter()
explanation = explainer.explain_instance(img, predict_wrapper, top_labels=1, hide_color=0, num_samples=1000)

# Extract and print explanation details
explanation_details = explanation.top_labels[0]
predicted_class = names[class_ids[0].item()]

print(f"Prediction: {predicted_class} (Confidence: {confidence[0].item():.2f})")
print("Explanation:")

for i, (prob, label) in enumerate(explanation_details):
    print(f"{i + 1}. {names[label]}: {prob:.2f}")