# -*- coding=utf-8 -*-
import models

def start():
    # setattr(models.VNode, "score", "0")

    modify_VNode = lambda name, bases, attrs: type(name, bases, attrs)

    newVNode = modify_VNode('newVNode', (models.VNode,), {'score': 0})
    a = newVNode()

    print(dir(newVNode))
    print newVNode, a.b
    pVNode = newVNode("start", None)
    pVNode.score = 2
    print(pVNode.get_name(), pVNode.score)

    print(hasattr(models.VNode, "score"))
    print(dir(models.VNode))


# http://blog.jobbole.com/21351/
# http://www.jb51.net/article/64123.htm
# http://www.jb51.net/article/87479.htm