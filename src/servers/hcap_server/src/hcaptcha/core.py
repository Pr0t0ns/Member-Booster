import os
import time
from typing import Optional
import cv2
import numpy as np

from .solutions import resnet, yolo


class ArmorCaptcha:

    label_alias = {
        "zh": {
            "自行车": "bicycle",
            "火车": "train",
            "卡车": "truck",
            "公交车": "bus",
            "巴士": "bus",
            "飞机": "airplane",
            "一条船": "boat",
            "船": "boat",
            "摩托车": "motorcycle",
            "垂直河流": "vertical river",
            "天空中向左飞行的飞机": "airplane in the sky flying left",
            "请选择天空中所有向右飞行的飞机": "airplanes in the sky that are flying to the right",
            "汽车": "car",
            "大象": "elephant",
            "鸟": "bird",
            "狗": "dog",
            "犬科动物": "dog",
            "一匹马": "horse",
            "长颈鹿": "giraffe",
        },
        "en": {
            "airplane": "airplane",
            "motorbus": "bus",
            "bus": "bus",
            "truck": "truck",
            "motorcycle": "motorcycle",
            "boat": "boat",
            "bicycle": "bicycle",
            "train": "train",
            "vertical river": "vertical river",
            "airplane in the sky flying left": "airplane in the sky flying left",
            "Please select all airplanes in the sky that are flying to the right": "airplanes in the sky that are flying to the right",
            "car": "car",
            "elephant": "elephant",
            "bird": "bird",
            "dog": "dog",
            "canine": "dog",
            "horse": "horse",
            "giraffe": "giraffe",
        },
    }

    BAD_CODE = {
        "а": "a",
        "е": "e",
        "e": "e",
        "i": "i",
        "і": "i",
        "ο": "o",
        "с": "c",
        "ԁ": "d",
        "ѕ": "s",
        "һ": "h",
        "у": "y",
        "р": "p",
        "ー": "一",
        "土": "士",
    }

    HOOK_CHALLENGE = "//iframe[contains(@title,'content')]"
    CHALLENGE_SUCCESS = "success"
    CHALLENGE_CONTINUE = "continue"
    CHALLENGE_CRASH = "crash"
    CHALLENGE_RETRY = "retry"
    CHALLENGE_REFRESH = "refresh"
    CHALLENGE_BACKCALL = "backcall"

    def __init__(
        self,
        dir_workspace: str = None,
        lang: Optional[str] = "en",
        onnx_prefix: str = None,
        debug=False,
        label=None,
        on_rainbow: Optional[bool] = True,
    ):

        self.action_name = "ArmorCaptcha"
        self.debug = debug
        self.dir_model = "src/servers/hcap_server/src/model"
        self.onnx_prefix = "yolo6s"
        self.path_objects_yaml = "src/servers/hcap_server/src/objects.yaml"
        self.on_rainbow = on_rainbow

        self.runtime_workspace = ""
        self.path_screenshot = ""
        self.lang = "en"
        self.label_alias: dict = self.label_alias[lang]

        self.label = label
        self.prompt = ""
        self.dir_workspace = dir_workspace if dir_workspace else "."

        self.threat = 0

        self.pom_handler = resnet.PluggableONNXModels(self.path_objects_yaml)
        self.label_alias.update(self.pom_handler.label_alias[lang])
        self.pluggable_onnx_models = self.pom_handler.overload(self.dir_model, self.on_rainbow)
        self.yolo_model = yolo.YOLO(self.dir_model, self.onnx_prefix)

    def _init_workspace(self):
        _prefix = (
            f"{time.time()}" + f"_{self.label_alias.get(self.label, '')}" if self.label else ""
        )
        _workspace = os.path.join(self.dir_workspace, _prefix)
        if not os.path.exists(_workspace):
            os.mkdir(_workspace)
        return _workspace

    def switch_solution(self):
        label_alias = self.label_alias.get(self.label)
        if self.pluggable_onnx_models.get(label_alias):
            return self.pluggable_onnx_models[label_alias]
        return self.yolo_model


    def challenge(self, images_task):
        model = self.switch_solution()
        ta = []
        answers = {}
        for image, task_key in images_task:
            result = model.solution(img_stream=image, label=self.label)
            if result:
                answers[task_key] = "true"
            else:
                answers[task_key] = "false"
        
        return answers

