#version 410


uniform vec3 camera_pos;



in vec4 shade_color;



out vec4 frag_color;




void main () {
    frag_color = shade_color;
    
}






