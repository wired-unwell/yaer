class Dog:
    """
    A small dumb class of animals.
    """

    sound: str

    def __init__(self, sound: str = "woof"):
        self.sound = sound

    def makeSound(self) -> None:
        print("I say " + self.sound)


dog = Dog("bark")
dog.makeSound()


class LoudDog(Dog):
    # Do not re-define __init__ if you want to inherit!

    def makeSound(self):
        sound = self.sound
        print(sound + " " + sound + " " + sound)


pitbul = LoudDog("bark")
pitbul.makeSound()
