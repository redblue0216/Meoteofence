import pluggy

hookspec = pluggy.HookspecMarker("myproject")
hookimpl = pluggy.HookimplMarker("myproject")


class MySpec:
    """A hook specification namespace."""

    @hookspec
    def a_func(self, arg1, arg2):
        """My special little hook that you can customize."""
        pass
    @hookspec
    def b_func(self,arg1,arg2):
        pass


class Plugin_1:
    """A hook implementation namespace."""

    @hookimpl
    def a_func(self, arg1, arg2):
        print("inside Plugin_1.myhook()")
        return arg1 + arg2


# class Plugin_2:
#     """A 2nd hook implementation namespace."""

    @hookimpl
    def b_func(self, arg1, arg2):
        print("inside Plugin_2.myhook()")
        return arg1 - arg2


# create a manager and add the spec
pm = pluggy.PluginManager("myproject")
pm.add_hookspecs(MySpec)
# register plugins
pm.register(Plugin_1())
# pm.register(Plugin_2())
# call our `myhook` hook
results = pm.hook.b_func(arg1=1, arg2=2)[0]
print(results)