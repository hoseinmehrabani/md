import torch  

# بارگذاری مدل  
model = torch.load('yolov5s.pt')  

# وقتی مدل دارای ساختار خاصی است، قبل از بارگذاری آن باید ساختار آن را تعریف کنید.  
# فرض کنید یک مدل CNN تعریف شده است:  
class MyModel(torch.nn.Module):  
    def __init__(self):  
        super(MyModel, self).__init__()  
        self.fc = torch.nn.Linear(10, 2)  # یک مثال ساده  

    def forward(self, x):  
        return self.fc(x)  

# بارگذاری مدل با ساختار  
model = MyModel()  
model.load_state_dict(torch.load('path_to_your_model.pt'))  
model.eval()  # تنظیم مدل به حالت ارزیابی
