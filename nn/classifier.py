import torch
import torchvision
from torch import nn
class Classifier(torch.nn.Module):
    def __init__(self, num_classes):
        super().__init__()    # Обращаемся к отцовскому конструктору nn.Module
        self.encoder = torchvision.models.mobilenet_v2(pretrained = True).features    # Обученная фигня
        # self.pooling = torch.nn.AdaptiveAvgPool2d()    # Пока не нужно в нашем случае
        self.linear_classifier = torch.nn.Linear(1280, num_classes)    # Отрезаем голову нашему отцовскому

        import json
        import os
        self.NAMES = None
        with open(os.path.join(os.path.dirname(__file__), "names.json"), "r") as f:
            self.NAMES = json.load(f)
                                                                                            # классификатору и вставляем наши 42 класса
    def forward(self, sample):
        final_feature_map = self.encoder(sample)    # Все слои и прочая муть от мобайлнета (backbone тоже разрешён)
        pooled_features = nn.functional.adaptive_avg_pool2d(final_feature_map, (1, 1))    # Объединяем слои
        flatten_features = torch.flatten(pooled_features, 1)    # Делаем одноразмерный тэнзор
        logits = self.linear_classifier(flatten_features) # argmax(logits) = pred_class    Отрезаем голову
        return logits

# indexes = [label_encoder.transform([ll]).item() for ll in labels]
# labels = [os.path.basename(x[0]) for x in os.walk("captures_dataset")][1:]
# {indexes[i]: labels[i] for i in range(len(labels))}
