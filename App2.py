import folium
import pandas as p
def mapping():

    map = folium.Map(
    location = [33.631344, 73.050895],
    tiles="Open Street Map",
    control_scale = True,
    zoom_start= 170,
    prefer_canvas = True, 
    )

    """This is the feature to add custom icon marker"""
    icon_url = "https://i.imgur.com/PkkOLqF.png"
    Home_icon = folium.features.CustomIcon(icon_url,icon_size=(28, 30))

    icon_p = "https://i.imgur.com/haQywc3.png"
    Petrol_icon = folium.features.CustomIcon(icon_p,icon_size=(28, 30))

    icon_s = "https://i.imgur.com/Zb5qg2c.png"
    Shop_icon = folium.features.CustomIcon(icon_s,icon_size=(28, 30))

    icon_n = "https://i.imgur.com/d5yKQxL.png"
    Nashta1_icon = folium.features.CustomIcon(icon_n,icon_size=(28, 30))


    #Create a FeatureGroup layer you can put things in it and handle them as a single layer
    fgvol = folium.FeatureGroup(name="Volcanoes") #single map-layer
    fg_my = folium.FeatureGroup(name = "My Radar")

    coordinates = [[33.631344, 73.050895],[33.63275915985772, 73.04955845704472],[33.630589334889265, 73.05023908322059]]

    for coord in coordinates:
        if(coord == [33.631344, 73.050895]):
            name = "My Home"
            newIcon = Home_icon
        elif(coord == [33.63275915985772, 73.04955845704472]):
            name = "Petrol"
            newIcon = Petrol_icon
        elif(coord == [33.630589334889265, 73.05023908322059]):
            name = "Jigar Nehari and Nashta"
            newIcon = Nashta1_icon
            
        fg_my.add_child(
            folium.Marker(location = coord, 
            popup=name,draggable=False, icon = newIcon)
            )
    
    DataFile = p.read_csv("Volcanoes_USA.txt")  #data readead from file to show coordincates on map
    lat = list(DataFile["LAT"])
    lon = list(DataFile["LON"])
    elev= list(DataFile["ELEV"])    #to show elevation eg: 2333m
    vName=list(DataFile["NAME"])

    #inner function that change color according to ----elevation--- values

    def color_changer(elev):
        if(elev<1000):
            return "green"
        elif(1000<=elev<3000):
            return "orange"
        else:
            return "red"      


    for lt, ln, el, vN in zip(lat, lon, elev, vName):
        fgvol.add_child(
            folium.CircleMarker(location = [lt,ln], 
            popup= str(el)+"m" ,draggable=False, 
            color =(color_changer(el)), 
            fill = True, fill_color = (color_changer(el)), fill_opacity = 1,
            radius=9, tooltip=vN )
            )

    fgpop = folium.FeatureGroup(name = "Population")
    fgpop.add_child(folium.GeoJson(data = open("world.json",encoding = "utf-8-sig").read(), 
    style_function= lambda x: {"fillColor":"green" if x["properties"]["POP2005"]< 10000000 else "orange" 
    if 10000000 <= x["properties"]["POP2005"] < 20000000 else "red"}))


    map.add_child(fgvol)                      #this is feature group objects that will show in layer control
    map.add_child(fg_my)
    map.add_child(fgpop)
    map.add_child(folium.LayerControl())
    map.save("myMap.html")

mapping()