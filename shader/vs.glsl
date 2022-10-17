#version 410

layout (location = 0) in vec3 vp;
layout (location = 1) in vec3 vn;
layout (location = 2) in vec2 vt;


uniform mat4 proj_mat, view_mat, model_mat;
uniform vec3 camera_pos;
uniform sampler2D image;

out vec4 shade_color;



vec3 phong(vec3 point, vec3 pointNorm, vec3 modelC, vec3 camPos  );

void main () {

    gl_Position = proj_mat * view_mat * model_mat * vec4 (vp, 1.0);
    
    shade_color = vec4(phong(vp, vn, vec3(1, 1, 1), camera_pos), 1.0);
 
}

vec3 phong( vec3 point, vec3 pointNorm, vec3 modelC, vec3 camPos)
{
    
    vec3 lightColor = vec3( 1.0, 1.0, 1.0 );
    float ambientStren = 0.1;
    float diffuseSten = 3.0;
    float specularSten = 0.1;

    vec3 Ka = ambientStren * lightColor;
    
    normalize( pointNorm );
    vec3 lightVector = camPos - point;
    normalize( lightVector );
    float diffuse = max(dot(pointNorm, lightVector), 0.0);
    vec3 Kd =  texture(image, vt).rgb * diffuse * diffuseSten;
    
    
    vec3 viewDir = normalize(camPos - point);
    vec3 reflectDir = normalize( reflect(-lightVector, pointNorm) );
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 10);
    vec3 Ks =  specularSten * spec * lightColor;
    
    return ( ( Ka + Kd + Ks ) *  modelC ); //need change for multi light
    
}
