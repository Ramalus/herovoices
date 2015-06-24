from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy import platform
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.animation import Animation

if platform != 'android':
    pass
else:
    from jnius import autoclass
    from time import sleep

import random
import hero_voices

__version__ = '0.8'

class HeroVoicesWidget(Widget):
    hero_names_rads=['Earthshaker','Sven','Tiny','Kunkka','Beastmaster','Dragon_Knight','Clockwerk','Omniknight','Huskar','Alchemist','Brewmaster','Treant_Protector','Io','Centaur_Warrunner','Timbersaw','Bristleback','Tusk','Elder_Titan','Legion_Commander','Earth_Spirit','Phoenix']
    hero_names_rada=['Anti-Mage', 'Drow_Ranger','Juggernaut','Mirana','Morphling','Phantom_Lancer', 'Vengeful_Spirit','Riki','Sniper','Templar_Assassin','Luna','Bounty_Hunter','Ursa','Gyrocopter','Lone_Druid','Naga_Siren','Troll_Warlord','Ember_Spirit']
    hero_names_radi=['Crystal_Maiden','Puck','Tinker','Windranger','Zeus','Storm_Spirit','Lina','Shadow_Shaman','Natures_Prophet','Enchantress','Jakiro','Chen','Silencer','Ogre_Magi','Rubick','Disruptor','Keeper_of_the_Light','Skywrath_Mage']
    hero_names_dirs=['Axe','Pudge','Sand_King','Slardar','Tidehunter','Wraith_King','Lifestealer','Night_Stalker','Doom','Spirit_Breaker','Lycan','Chaos_Knight','Undying','Magnus','Abaddon']
    hero_names_dira=['Bloodseeker','Shadow_Fiend','Razor','Venomancer','Faceless_Void','Phantom_Assassin','Viper','Clinkz','Broodmother','Weaver','Spectre','Meepo','Nyx_Assassin','Slark','Medusa','Terrorblade']
    hero_names_diri=['Bane','Lich','Lion','Witch_Doctor','Enigma','Necrophos','Warlock','Queen_of_Pain','Death_Prophet','Pugna','Dazzle','Leshrac','Dark_Seer','Batrider','Ancient_Apparition','Invoker','Outworld_Devourer','Shadow_Demon','Visage']

    hero_names = [hero_names_rads, hero_names_rada, hero_names_radi, hero_names_dirs, hero_names_dira, hero_names_diri]

    def on_input_focus(self, instance, value):
        if value:
            print('User focused', instance)
            instance.text=''
        else:
            print('User defocused', instance)

    def on_input_text(self, instance, value):
        #print('The Widget', instance, 'has', value)
        for child in self.buttons:
            self.ids.glayout.remove_widget(child)
            if value.lower() in child.background_normal.replace('images/', '').replace('.png', '').replace('_',' ').lower():
                self.ids.glayout.add_widget(child)

    def on_button_width(self, instance, value):
        instance.height=instance.width*0.5625

    def __init__(self):
        Widget.__init__(self)
        self.ids['tInput'].bind(focus=self.on_input_focus)
        self.ids['tInput'].bind(text=self.on_input_text)
        self.buttons = []
        for name in self.hero_names:
            for hero_name in name:
                # height=self.height*0.10157,
                bt = Button(text='', background_normal='images/%s.png'%hero_name,  width=Window.width/3.25, size_hint_x=None, size_hint_y=None, opacity=0.8)
                bt.height=bt.width*0.5620
                print(bt.width, bt.height)
                bt.bind(on_press=lambda x, n=hero_name: self.button_press(n))
                bt.bind(width=self.on_button_width)
                self.buttons.append(bt)

        self.buttons.sort(key=lambda x: x.background_normal)
        for bt in self.buttons:
            self.ids.glayout.add_widget(bt)

        if platform == 'android':
             self.MediaPlayer=autoclass('android.media.MediaPlayer')
             self.player = self.MediaPlayer()

        self.ids.glayout.bind(minimum_height=self.ids.glayout.setter('height'))

    def track_progress(self, dt):
        pbar = self.ids['pbar']
        pos = self.sound.get_pos()
        pbar.max = self.sound.length
        pbar.value = pos

    def track_progress_android(self, dt):
        pbar = self.ids['pbar']
        pos = self.player.getCurrentPosition()
        pbar.max = self.player.getDuration()
        pbar.value = pos

    def button_press(self, hero_name):
        for hero in hero_voices.voices:
            if hero_name in hero['name']:
                if platform == 'android':
                    if not self.player.isPlaying():
                        self.player.reset()
                        self.player.setDataSource(random.choice(hero['voices']))
                        self.player.prepare()
                        self.player.start()
                        Clock.schedule_interval(self.track_progress_android, 0.1)
                else:
                    self.sound = SoundLoader.load(random.choice(hero['voices']))
                    self.sound.volume=0.1
                    self.sound.play()
                    Clock.schedule_interval(self.track_progress, 0.1)

class HeroVoicesApp(App):
    def build(self):
        heroVoices = HeroVoicesWidget()
        return heroVoices

    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass 

if __name__ == '__main__':
    # Window.fullscreen = True
    HeroVoicesApp().run()
