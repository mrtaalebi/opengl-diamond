# version 330

in vec3 frag_pos;
in vec3 normal;

out vec4 frag_color;

void main()
{
    vec3 obj_color = vec3(0.00, 0.55, 0.85);


    vec3 light_1 = vec3(0.90, 1.0, 1.0);
    vec3 pos_1 = vec3(10.0, 10.0, 2.0);

    float ambient_str = 0.1;
    vec3 ambient = ambient_str * light_1;

    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(pos_1 - frag_pos);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = diff * light_1;

    float specular_str = 0.5;
    vec3 view_dir = normalize(vec3(0.0, 0.0, -10.0) - frag_pos);
    vec3 reflect_dir = reflect(-light_dir, norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    vec3 specular = specular_str * spec * light_1;

    vec3 result_1 = (ambient + diffuse + specular) * obj_color;


    vec3 light_2 = vec3(0.95, 0.95, 0.65);
    vec3 pos_2 = vec3(-10.0, -5.0, -1.0);

    float ambient_str_2 = 0.10;
    vec3 ambient_2 = ambient_str_2 * light_2;

    vec3 light_dir_2 = normalize(pos_2 - frag_pos);
    float diff_2 = max(dot(norm, light_dir_2), 0.0);
    vec3 diffuse_2 = diff_2 * light_2;

    float specular_str_2 = 0.50;
    vec3 reflect_dir_2 = reflect(-light_dir_2, norm);
    float spec_2 = pow(max(dot(view_dir, reflect_dir_2), 0.0), 32);
    vec3 specular_2 = specular_str_2 * spec_2 * light_2;

    vec3 result_2 = (ambient_2 + diffuse_2 + specular_2) * obj_color;

    vec3 result = result_1 + result_2;
    frag_color = vec4(result, 1.0);
}
