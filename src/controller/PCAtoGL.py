class ViewPortHandler():
    def __init__(self, view_port, model):
        view_port.mesh = model.mesh
        view_port.img = model.diffuse