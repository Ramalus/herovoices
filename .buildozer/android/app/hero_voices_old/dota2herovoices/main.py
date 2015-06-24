from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy import platform

if platform != 'android':
    pass
else:
    from jnius import autoclass
    from time import sleep

import random
import hero_voices

from functools import partial

class MainUI(Widget):
    xhint = NumericProperty(0.25)
    yhint = NumericProperty(0.75)
    ysize = NumericProperty(70)
    xsize = NumericProperty(110)
    hero_names_rads=['Earthshaker','Sven','Tiny','Kunkka','Beastmaster','Dragon_Knight','Clockwerk','Omniknight','Huskar','Alchemist','Brewmaster','Treant_Protector','Io','Centaur_Warrunner','Timbersaw','Bristleback','Tusk','Elder_Titan','Legion_Commander','Earth_Spirit','Phoenix']
    hero_names_rada=['Anti-Mage', 'Drow_Ranger','Juggernaut','Mirana','Morphling','Phantom_Lancer', 'Vengeful_Spirit','Riki','Sniper','Templar_Assassin','Luna','Bounty_Hunter','Ursa','Gyrocopter','Lone_Druid','Naga_Siren','Troll_Warlord','Ember_Spirit']
    hero_names_radi=['Crystal_Maiden','Puck','Tinker','Windranger','Zeus','Storm_Spirit','Lina','Shadow_Shaman','Natures_Prophet','Enchantress','Jakiro','Chen','Silencer','Ogre_Magi','Rubick','Disruptor','Keeper_of_the_Light','Skywrath_Mage']
    hero_names_dirs=['Axe','Pudge','Sand_King','Slardar','Tidehunter','Wraith_King','Lifestealer','Night_Stalker','Doom','Spirit_Breaker','Lycan','Chaos_Knight','Undying','Magnus','Abaddon']
    hero_names_dira=['Bloodseeker','Shadow_Fiend','Razor','Venomancer','Faceless_Void','Phantom_Assassin','Viper','Clinkz','Broodmother','Weaver','Spectre','Meepo','Nyx_Assassin','Slark','Medusa','Terrorblade']
    hero_names_diri=['Bane','Lich','Lion','Witch_Doctor','Enigma','Necrophos','Warlock','Queen_of_Pain','Death_Prophet','Pugna','Dazzle','Leshrac','Dark_Seer','Batrider','Ancient_Apparition','Invoker','Outworld_Devourer','Shadow_Demon','Visage']

    def __init__(self):
        Widget.__init__(self)
        self.create_buttons(self.hero_names_rads, self.ids.stlay_ras)
        self.create_buttons(self.hero_names_rada, self.ids.stlay_raa)
        self.create_buttons(self.hero_names_radi, self.ids.stlay_rai)
        self.create_buttons(self.hero_names_dirs, self.ids.stlay_dis)
        self.create_buttons(self.hero_names_dira, self.ids.stlay_dia)
        self.create_buttons(self.hero_names_diri, self.ids.stlay_dii)
        #create rest of the buttons
        if platform == 'android':
            self.MediaPlayer=autoclass('android.media.MediaPlayer')
            self.player = self.MediaPlayer()
    
    def create_buttons(self, hero_names, layout):
        for name in hero_names:
            #height=self.ysize,width=self.xsize,
            #name
            bt = Button(text='',size_hint=(0.3,0.05),background_normal='images/%s.png'%name,text_size=(None,None),vlign='bottom')
            bt.bind(on_press=lambda x, n=name: self.button_press(n))
            bt.text_size=(None, bt.height)
            layout.add_widget(bt)

    def button_press(self, hero_name):
        for hero in hero_voices.voices:
            if hero_name in hero['name']:
                if platform == 'android':
                    if not self.player.isPlaying():
                        self.player.reset()
                        self.player.setDataSource(random.choice(hero['voices']))
                        self.player.prepare()
                        self.player.start()
                else:
                    sound = SoundLoader.load(random.choice(hero['voices']))
                    sound.play()

class Dota2HeroVoicesApp(App):
    def build(self):
        return MainUI()

if __name__== '__main__':
    Dota2HeroVoicesApp().run()
