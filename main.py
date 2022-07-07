import math

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr


def draw_diamond():
    vertices, indices = [], []

    unit = 2*math.pi / 8

    # bottom point
    for i in range(8):
        tetha = i * unit
        x_r = math.cos(tetha + unit / 2)
        y_r = math.cos(tetha + unit / 2)
        vertices += [+0.00, +0.00, -0.70, 1.00, 0.50, 0.20, x_r, y_r, (x_r**2 + y_r**2)**0.5 * 3/5]

    # 1st circle
    for i in range(8):
        tetha = i * unit
        x, x_l, x_r = math.cos(tetha), math.cos(tetha - unit / 2), math.cos(tetha + unit / 2)
        y, y_l, y_r = math.sin(tetha), math.sin(tetha - unit / 2), math.sin(tetha + unit / 2)
        vertices += [x * 0.30, y * 0.30, -0.20, 0.50, 0.50, 0.90, x_l, y_l, (x_l**2 + y_l**2)**0.5 * 0.6]
        vertices += [x * 0.30, y * 0.30, -0.20, 0.50, 0.50, 0.90, x_r, y_r, (x_r**2 + y_r**2)**0.5 * 0.6]

    for i in range(0, 7):
        indices += [i * 2 + 8 + 1, i * 2 + 8 + 2, i]
    indices += [23, 8, 7]

    # 2nd circle
    for i in range(8):
        tetha = i * unit
        x, x_l, x_ll, x_r, x_rr = math.cos(tetha), math.cos(tetha - unit / 2), math.cos(tetha - unit), math.cos(tetha + unit / 2), math.cos(tetha + unit)
        y, y_l, y_ll, y_r, y_rr = math.sin(tetha), math.sin(tetha - unit / 2), math.sin(tetha - unit), math.sin(tetha + unit / 2), math.sin(tetha + unit)
        vertices += [x_l * 0.20, y_l * 0.20, +0.00, 0.50, 0.50, 0.20, x_ll, y_ll, (x_ll**2 + y_ll**2)**0.5 * 0.55]
        vertices += [x_l * 0.20, y_l * 0.20, +0.00, 0.50, 0.50, 0.20, x_l, y_l, (x_l**2 + y_l**2)**0.5 * 0.45]
        vertices += [x_l * 0.20, y_l * 0.20, +0.00, 0.50, 0.50, 0.20, x, y, (x**2 + y**2)**0.5 * 0.55]
        vertices += [x_l * 0.20, y_l * 0.20, +0.00, 0.50, 0.50, 0.20, 0, 0, 1]

        vertices += [x * 0.30, y * 0.30, -0.20, 0.50, 0.50, 0.20, x_l, y_l, (x_l**2 + y_l**2)**0.5 * 0.45]
        vertices += [x * 0.30, y * 0.30, -0.20, 0.50, 0.50, 0.20, x, y, (x**2 + y**2)**0.5 * 0.55]
        vertices += [x * 0.30, y * 0.30, -0.20, 0.50, 0.50, 0.20, x_r, y_r, (x_r**2 + y_r**2)**0.5 * 0.45]

    for i in range(1, 8):
        indices += [24 + i * 7 - 5, 24 + i * 7, 24 + i * 7 - 2]
    indices += [24, 75, 78]

    for i in range(1, 8):
        indices += [24 + i * 7 - 1, 24 + i * 7 + 4, 24 + i * 7 + 1]
    indices += [25, 28, 79]

    for i in range(0, 8):
        indices += [27, 27 + i * 7 + 7, 27 + i * 7 + 7 * 2]

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    return vertices, indices


def setup_shader(vertices, indices):
    with open('diamond.vs', 'r') as f:
        vertex_src = f.read()

    with open('diamond.frag', 'r') as f:
        fragment_src = f.read()

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(0))

    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(12))

    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 36, ctypes.c_void_p(24))

    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    return shader


def setup_window():
    def window_resize(window, width, height):
        glViewport(0, 0, width, height)

    if not glfw.init():
        raise Exception("glfw can not be initialized!")
    window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    glfw.set_window_pos(window, 400, 200)
    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)
    return window


def run(window, shader, indices):
    rotation_loc = glGetUniformLocation(shader, "rotation")

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        rot_x = pyrr.Matrix44.from_x_rotation(math.sin(2 * glfw.get_time()) * math.pi / 8 + math.pi / 2)
        rot_y = pyrr.Matrix44.from_y_rotation(math.cos(2 * glfw.get_time()) * math.pi / 8 + math.pi / 4)
        rot_z = pyrr.Matrix44.from_z_rotation(math.sin(glfw.get_time()) * math.pi / 8)

        glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, pyrr.matrix44.multiply(pyrr.matrix44.multiply(rot_x, rot_y), rot_z))

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()


def main():
    vertices, indices = draw_diamond()
    window = setup_window()
    shader = setup_shader(vertices, indices)
    run(window, shader, indices)


if __name__ == '__main__':
    main()
