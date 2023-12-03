import os
import torch
from torchvision import transforms
from .classifier import Classifier
from PIL import Image

def get_result(fp_to_dir):
    png_files = [os.path.join(fp_to_dir, f) for f in os.listdir(fp_to_dir) if f.endswith('.png')]
    num = len(png_files)
    sum = 0.
    for fp in png_files:
        name = get_name(fp)
        if name in ["captures.departure.arrival", "captures.departure_hoz.arrival_hoz", "captures.departure_pass.arrival_pass"]:
            sum+=1.
        else:
            sum += 0.1
    return sum / num

def get_name(fp_to_img):
    model = Classifier(num_classes=256)
    WEIGHTS = os.path.join(os.path.dirname(__file__), "best.pt")
    if torch.cuda.is_available():
        model.load_state_dict(torch.load(WEIGHTS))
    else:
        model.load_state_dict(torch.load(WEIGHTS, map_location=torch.device('cpu')))

    input_image = Image.open(fp_to_img)
    preprocess = transforms.Compose([transforms.ToTensor(), transforms.CenterCrop(224),
                                     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        model.eval()
        output = model(input_batch)

    return model.NAMES[str(output.argmax(1)[0].item())]