from appJar import gui
from IP import IP
def drag(widget):
    global dragged
    #print("Dragged from:", widget)
    dragged = widget

def drop(widget):
    global dragged
    #print("Dropped on:", widget)
    if len(widget) == 2:
        routes.insert(int(widget[1]),routes.pop(int(dragged[1])))
    if widget == 'delete':
        routingtable.pop(routes[int(dragged[1])])
        routes.pop(int(dragged[1]))
    draw_routes()
    dragged = None

app = gui("Router")

app.setFont(20)
dragged = None
routingtable = {
    ('22.33.44.1', '/24'):(0, None),
    ('22.33.55.1', '/24'):(1, None),
    ('0.0.0.0', '/0'):(2, IP('22.33.1.1'))
}
routes = [('22.33.44.1', '/24'),('22.33.55.1', '/24'),('0.0.0.0', '/0')]


frame = 'Routes'

def draw_routes():
    app.openLabelFrame(frame)
    app.emptyCurrentContainer()
    n = 0
    for route in routes:
        app.addLabel('a'+str(n), route[0]+route[1] + '    ', column=0, row=n)
        app.addLabel('b'+str(n),'   -->   ', column=1, row=n)
        if routingtable[route][1]:
            dest = routingtable[route][1].str
        else:
            dest = 'DC'
        app.addLabel('c'+str(n),  '    IF' +str(routingtable[route][0])+'    ', column=2, row=n)
        app.addLabel('d'+str(n),dest, column=3, row=n)
        app.setLabelDragFunction('a'+str(n), [drag, drop])
        app.setLabelDragFunction('b'+str(n), [drag, drop])
        app.setLabelDragFunction('c'+str(n), [drag, drop])
        app.setLabelDragFunction('d'+str(n), [drag, drop])
        n+= 1
    app.stopLabelFrame()
        

def add_route(button):
    if button == 'Cancel':
        app.hideSubWindow('one')
    else:
        route = (app.getEntry('Route: '), app.getEntry('Subnet: '))
        destination = app.getEntry('Destination: ')
        if destination == 'DC':
            destination = None
        else:
            destination = IP(destination)
        interface = app.getEntry('Interface: ')
        if interface[0:2].upper() == 'IF':
            interface = interface[2:]
        dest = (int(interface), destination)
        routes.append(route)
        routingtable[route] = dest
        app.hideSubWindow('one')
    draw_routes()



def add(button):
    app.showSubWindow('one')

app.startSubWindow("one", modal=True)
app.addLabel("label1", "Configure new route")
app.addLabelEntry('Route: ')
app.addLabelEntry('Subnet: ')
app.addLabelEntry('Destination: ')
app.addLabelEntry('Interface: ')
app.addHorizontalSeparator()
app.addButtons(['Continue', 'Cancel'], add_route)
app.stopSubWindow()
app.addLabel('title', 'Router configuration')
app.startLabelFrame(frame)
app.addLabel('loading', 'Loading')
app.stopLabelFrame()
draw_routes()
app.startFrame('asdf')
app.addLabel('delete', 'Delete', column=0, row=len(routes))
app.addButton('Add route', add, column=1,  row=len(routes))
app.stopFrame()

app.go()