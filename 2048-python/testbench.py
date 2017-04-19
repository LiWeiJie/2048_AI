#! /usr/bin/python3
# -*- coding:utf-8 -*-  

import importlib

class Testbench(object):
    def start(self, moduleName):
        module=importlib.import_module(moduleName)
        module_dir=dir(module)
        #print("module content %s"%module_dir)
        for element in module_dir:
            if(isinstance(element, object) and (element.startswith('Test'))):
                print("%s is class"%(element))
                TestSuitClass = getattr(module, element)
                
                #instantiate an object
                obj=TestSuitClass()
                #根据一个类，去找它的以“test_”开头的成员函数，并自动执行
                #get function list from a class
                func_names=dir(TestSuitClass)
                for func_name in func_names:
                    if func_name.startswith('test_'):
                        print("run func %s automatically"%func_name)
                        #get function
                        func=getattr(obj,func_name)
                        #call this function
                        func()
        return



if __name__=="__main__":
    tb = Testbench()
    tb.start("grid")
    tb.start("tile")
    tb.start("play")
    tb.start("ai")