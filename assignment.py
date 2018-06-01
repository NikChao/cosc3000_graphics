from OpenGL.GL import *
import math
import numpy as np
import time
import imgui

import magic
# We import the 'lab_utils' module as 'lu' to save a bit of typing while still clearly marking where the code came from.
import lab_utils as lu

g_cameraDistance = 1.0
g_cameraYawDeg = 0.0
g_cameraPitchDeg = 0.0
g_yFovDeg = 45.0

g_lightYaw = 25.0
g_lightYawSpeed = 0.0#145.0
g_lightPitch = -75.0
g_lightPitchSpeed = 0.0#30.0
g_lightDistance = 250.0
g_lightColourAndIntensity = lu.vec3(0.9, 0.9, 0.6)
g_ambientLightColourAndIntensity = lu.vec3(0.1)

white = (1, 1, 1, 1)

def draw_rectangle(vertices, transform, colour, lightPosition):
    magic.drawVertexDataAsTrianglesColour([vertices[0], vertices[1], vertices[3]], transform, colour, lightPosition)
    magic.drawVertexDataAsTrianglesColour([vertices[1], vertices[2], vertices[3]], transform, colour, lightPosition)

def draw_base_court(transform, lightPosition):
    court_vertices = [
        [0.52,  0.5, 0.0], # top right
        [0.52, -0.5, 0.0], # bottom right
        [-0.06, -0.5, 0.0], # bottom left
        [-0.06,  0.5, 0.0]  # top left
    ]

    base = [
        [0.75,  0.75, -0.01], # top right
        [0.75, -0.75, -0.01], # bottom right
        [-0.75, -0.75, -0.01], # bottom left
        [-0.75,  0.75, -0.01]  # top left
    ]
    draw_rectangle(base, transform, (0, 0, 1, 0.7), lightPosition)

    borders = [
        [
            [-0.07,  0.5, 0.0], # top right
            [-0.07, -0.5, 0.0], # bottom right
            [-0.06, -0.5, 0.0], # bottom left
            [-0.06,  0.5, 0.0]  # top left
        ],
        [
            [0.53,  0.5, 0.0], # top right
            [0.53, -0.5, 0.0], # bottom right
            [0.52, -0.5, 0.0], # bottom left
            [0.52,  0.5, 0.0]  # top left
        ],
        [
            [0.53,  -0.5, 0.0], # top right
            [0.53, -0.51, 0.0], # bottom right
            [-0.07, -0.51, 0.0], # bottom left
            [-0.07,  -0.5, 0.0]  # top left
        ],
        [
            [0.53,  0.51, 0.0], # top right
            [0.53, 0.5, 0.0], # bottom right
            [-0.07, 0.5, 0.0], # bottom left
            [-0.07,  0.51, 0.0]  # top left
        ]
    ]

    draw_rectangle(court_vertices, transform, (0.31, 0.1, 0.1, 1), lightPosition)
    draw_rectangle(court_vertices, transform, (0.31, 0.1, 0.1, 1), lightPosition)
    for border in borders:
        draw_rectangle(border, transform, white, lightPosition)

def draw_net(transform, lightPosition):

    net_cols = []
    net_rows = []

    left = -0.06
    right = 0.52
    top = 0.05
    bottom = 0
    
    nets = [
        [
            [right, -0.01, top],
            [right, -0.01, bottom],
            [left, -0.01, bottom],
            [left, -0.01, top]
        ],
        [
            [right, 0.01, top],
            [right, 0.01, bottom],
            [left, 0.01, bottom],
            [left, 0.01, top]
        ]
    ]


    net_sides = [
        [
            [left, 0.01, top],
            [right, -0.01, top],
            [right, 0.01, top],
            [left, -0.01, top]
        ],
        [
            [right, 0.01, top],
            [right, -0.01, bottom],
            [right, 0.01, bottom],
            [right, -0.01, top]
        ],
        [
            [left, 0.01, top],
            [left, -0.01, bottom],
            [left, 0.01, bottom],
            [left, -0.01, top]
        ]
    ]

    for side in net_sides:
        draw_rectangle(side, transform, (1, 1, 1, 1), lightPosition)
    for side in nets:
        draw_rectangle(side, transform, (0, 0, 0, 1), lightPosition)

def draw_lines(transform, lightPosition):
    middle_line = [
        [0.52,  0.005, 0.0], # top right
        [0.52, -0.005, 0.0], # bottom right
        [-0.06, -0.005, 0.0], # bottom left
        [-0.06,  0.0005, 0.0]  # top left
    ]

    service_line_split = [
        [0.235,  0.255, 0.0], # top right
        [0.235, -0.255, 0.0], # bottom right
        [0.225, -0.255, 0.0], # bottom left
        [0.225,  0.255, 0.0]  # top left
    ]

    service_line_split = [
        [0.235,  0.255, 0.0], # top right
        [0.235, -0.255, 0.0], # bottom right
        [0.225, -0.255, 0.0], # bottom left
        [0.225,  0.255, 0.0]  # top left
    ]

    hashes = [
        [
            [0.235,  -0.49, 0.0], # top right
            [0.235, -0.5, 0.0], # bottom right
            [0.225, -0.5, 0.0], # bottom left
            [0.225,  -0.49, 0.0]  # top left
        ],
        [
            [0.235,  0.5, 0.0], # top right
            [0.235, 0.49, 0.0], # bottom right
            [0.225, 0.49, 0.0], # bottom left
            [0.225,  0.5, 0.0]  # top left
        ],
    ]

    for h in hashes:
        draw_rectangle(h, transform, white, lightPosition)

    service_line_top = [
        [0.46,  0.255, 0.0], # top right
        [0.46, 0.250, 0.0], # bottom right
        [0.0, 0.250, 0.0], # bottom left
        [0.0,  0.255, 0.0]  # top left
    ]

    service_line_bottom = [
        [0.46,  -0.255, 0.0], # top right
        [0.46, -0.250, 0.0], # bottom right
        [0.0, -0.250, 0.0], # bottom left
        [0.0,  -0.255, 0.0]  # top left
    ]

    tracks = [
        [
            [0.005,  0.5, 0.0], # top right
            [0.005, -0.5, 0.0], # bottom right
            [-0.0005, -0.5, 0.0], # bottom left
            [-0.005,  0.5, 0.0]  # top left
        ],
        [
            [0.465,  0.5, 0.0], # top right
            [0.465, -0.5, 0.0], # bottom right
            [0.455, -0.5, 0.0], # bottom left
            [0.455,  0.5, 0.0]  # top left
        ]
    ]

    draw_rectangle(middle_line, transform, white, lightPosition)
    draw_rectangle(service_line_split, transform, white, lightPosition)
    draw_rectangle(service_line_top, transform, white, lightPosition)
    draw_rectangle(service_line_bottom, transform, white, lightPosition)
    for track in tracks:
        draw_rectangle(track, transform, white, lightPosition)

def draw_court(transform, lightPosition):
    draw_base_court(transform, lightPosition)
    draw_lines(transform, lightPosition)
    draw_net(transform, lightPosition)

# This function is called by the 'magic' to draw a frame width, height are the size of the frame buffer, or window
def renderFrame(uiWidth, width, height):
    global g_triangleVerts
    global g_cameraDistance
    global g_cameraYawDeg
    global g_cameraPitchDeg
    global g_yFovDeg

    global g_lightYaw
    global g_lightDistance
    global g_lightPitch

    # This configures the fixed-function transformation from Normalized Device Coordinates (NDC)
    # to the screen (pixels - called 'window coordinates' in OpenGL documentation).
    #   See: https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
    glViewport(0, 0, width, height)
    # Set the colour we want the frame buffer cleared to, 
    glClearColor(0.2, 0.5, 0.1, 1.0)
    # Tell OpenGL to clear the render target to the clear values for both depth and colour buffers (depth uses the default)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)



    viewToClipTransform = lu.make_perspective(g_yFovDeg, width/height, 0.1, 50.0)

    eyePos = lu.Mat3(lu.make_rotation_y(math.radians(g_cameraYawDeg))) * lu.Mat3(lu.make_rotation_x(math.radians(g_cameraPitchDeg))) * [0,0,g_cameraDistance]
    worldToViewTransform = magic.make_lookAt(eyePos, [0,0,0], [0,1,0])

    worldToClipTransform = viewToClipTransform * worldToViewTransform

    lightRotation = lu.Mat3(lu.make_rotation_y(math.radians(g_lightYaw))) * lu.Mat3(lu.make_rotation_x(math.radians(g_lightPitch))) 
    lightPosition = [0.02, 0, 0] + lu.vec3(0,23, 0.2)

    draw_court(worldToClipTransform, lightPosition);
    lu.drawSphere([0.23, -0.45, 0.1, 0], 0.007, [0,1,0,0.5], viewToClipTransform, worldToViewTransform)
    lu.drawSphere(lightPosition, 0.01, [1,1,0,1], viewToClipTransform, worldToViewTransform)

def drawUi(width, height):
    global g_triangleVerts
    global g_cameraDistance
    global g_cameraYawDeg
    global g_cameraPitchDeg
    global g_yFovDeg

    imgui.push_item_width(200)
    _,g_cameraDistance = imgui.slider_float("CameraDistance", g_cameraDistance, 1.00, 20.0)
    _,g_yFovDeg = imgui.slider_float("Y-Fov (Deg)", g_yFovDeg, 1.00, 90.0)
    _,g_cameraYawDeg = imgui.slider_float("Camera Yaw (Deg)", g_cameraYawDeg, -180.00, 180.0)
    _,g_cameraPitchDeg = imgui.slider_float("Camera Pitch (Deg)", g_cameraPitchDeg, -89.00, 89.0)
    imgui.pop_item_width()

magic.runProgram("s4357755 - Graphics assignment", 640, 480, renderFrame, None, drawUi)
