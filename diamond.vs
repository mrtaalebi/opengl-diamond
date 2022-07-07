# version 330

layout(location = 0) in vec3 a_position;
layout(location = 2) in vec3 a_normal;

uniform mat4 rotation;

out vec3 frag_pos;
out vec3 normal;

void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
    frag_pos = vec3(gl_Position);
    normal = vec3(rotation * vec4(a_normal, 1.0));
}
