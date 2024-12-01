# Alien Invasion

__Alien Invasion__ is a well-known game where the player must shoot down a fleet of alien ships.

The game is based on a task 14-6 from Eric Mathis's [book](https://disk.yandex.ru/i/ttWTX-bEfT5LrQ) "Learning Python. Game programming, data visualization, web applications"

The goal of this game is to enhance practical programming abilities in Python.

# Gameplay

After starting the game, we are greeted by the main menu screen, with the option to start the game, view its rules and leave it
 
When you click on the Start Game button, we go directly into battle.
The gameplay involves the player shooting at alien ships, while the aliens return fire.


<img src="gif/main_menu.gif" alt="Описание изображения" width="600" height="300"/>

## Key Features

To make the game not boring, I added various game elements and mechanisms to it:

- A variety of game objects;   
- Transitions to a new level;
- Scoring and keeping the record;
- Sound effects;
- Some graphical effects.

Let's consider each item separately!

### Game ships

All game elements that affect the gameplay can be divided into two categories: **ships** and **shells**. These elements are different for the player and the aliens, which gives the game a special dynamic.




The player has the opportunity to play on 3 ships, each of which is better after destroying the previous one. Thus, the player has 3 attempts in one game. 
 Let's look at each of them:

| Image | Description                                                  |
|-------|--------------------------------------------------------------|
|<img src="images/ship1.png" alt="Описание изображения" width="50" height="50"/>|The player's standard ship, equipped with one gun.|
|<img src="images/ship2.png" alt="Описание изображения" width="50" height="50"/>|An improved ship with two side guns that fire simultaneously.|
|<img src="images/ship3.png" alt="Описание изображения" width="50" height="50"/>|The most powerful ship with three guns and a special projectile for one of them.|

The player's ships can be destroyed in the following situations:

1.  when they are hit by alien bullets;

2.  as a result of a collision with aliens;

3. when the alien fleet reaches the bottom of the screen.

---
In turn, alien ships have three types:

| Image | Description                                                  |
|-------|--------------------------------------------------------------|
|<img src="images/alien.png" alt="Описание изображения" width="60" height="50"/>|A standard alien ship. It is destroyed immediately after being hit by a player's bullet.|
|<img src="images/boosted_alien.png" alt="Описание изображения" width="60" height="50"/>|A boosted alien ship. It is destroyed after several hits by the player's bullet.|
|<img src="images/damaged_alien.png" alt="Описание изображения" width="60" height="50"/>|A system of hit points is provided for the armored ship. If a player hits it with a bullet,<br/> the ship is not completely destroyed, but gets damaged |


Each of them is capable of firing identical projectiles at the player.


### Projectiles

Usually, the player shoots ordinary bullets that can destroy one alien. However, when he has a third ship at his
disposal, he will receive a new gun with a special type of red projectile. This projectile is capable of shooting 
through all the aliens it hits.

| Image                                                                                     | Description                                    |
|-------------------------------------------------------------------------------------------|------------------------------------------------|
| <img src="images/standart_bullet.png" alt="Описание изображения" width="37" height="47"/> | A standard projectile destroys one alien       |
| <img src="images/boosted_bullet.png" alt="Описание изображения" width="37" height="47"/>  | Boosted projectile hits the entire alien fleet |

<img src="gif/red_projectile.gif" alt="Описание изображения" width="600" height="300"/>

In addition, a new type of weapon has been added to the game — an **aerial bomb**, available to all ships. 

| Image                                                                              |Description|
|------------------------------------------------------------------------------------|--|
| <img src="images/air_bomb.png" alt="Описание изображения" width="60" height="50"/> |An aerial bomb falls from above and destroys a group of aliens |
It can be used if
the player decides to bypass the alien fleet and attack them from above. Each aerial bomb is capable of destroying a 
group of aliens. If it hits an armored alien, it will immediately destroy it, otherwise it will cause damage to it.

<img src="gif/air_bomb.gif" alt="Описание изображения" width="600" height="300"/>

--- 
Alien ships, in turn, have one type of projectile that is equally fatal even with a single hit on the player. However,
the aliens periodically fire projectiles in random order, which guarantees return fire at the player until he completely
destroys them.

| Image                                                                                  |Description|
|----------------------------------------------------------------------------------------|--|
| <img src="images/alien_bullet.png" alt="Описание изображения" width="40" height="60"/> |The alien's projectile destroys the player's ship with a single hit  |

<img src="gif/alien_bullet.gif" alt="Описание изображения" width="600" height="300"/>

### Transitions to a new level

---
The transition to a new level occurs after the player destroys the alien fleet. 
When you move to a new level of the game, the difficulty increases. Here's how it happens:

1. All game objects such as bullets, projectiles and ships become faster. 
2. The number of aliens who can shoot at you and have armor increases. 

#### The edge cases:
- if the player's ship collides with the last alien, then the hit counts and the player moves to the next level, but loses
the ship;

<img src="gif/next_level.gif" alt="Описание изображения" width="600" height="300"/>

- if the alien fleet reaches the bottom edge of the screen, the player loses the ship and remains at the same level.

<img src="gif/return_level.gif" alt="Описание изображения" width="600" height="300"/>


### Scoring and keeping the record

---
In this game, points are awarded for each successful shot by the player at an alien ship or projectile. Not only direct
hits are taken into account, but also shots fired with boosted bullets and aerial bombs. The record of the game is
always displayed at the top of the window and saved in the .txt file of the project.

The higher the level of the game, the more points are awarded for each hit.
#### The edge cases 

- if the alien fleet reaches the bottom edge of the screen, the all points gained disappear.

## Game States

| Main Menu                                                                             | Game process                                                                             | Pause                                                                             | About It                                                                             |
|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| <img src="images/main_menu.png" alt="Описание изображения" width="300" height="150"/> | <img src="images/game_process.png" alt="Описание изображения" width="300" height="150"/> | <img src="images/pause.png" alt="Описание изображения" width="300" height="150"/> | <img src="images/about_it.png" alt="Описание изображения" width="300" height="150"/> |

## Managing game objects

For state **Main menu**:

| Key       | Description|
|-----------|------------|
| Enter     |            |
| Esc       |            |
| F1        |            |


For state **Game process**:

| Key       | Description|
|-----------|------------|
| Esc       |            |
| P         |            |
| Shift     |            |
| Space     |            |

For state **Pause**:

| Key           | Description|
|---------------|------------|
| Enter/P/Space |            |
| Esc           |            |
| Backspace     |            |


For state **About It**:

| Key       | Description |
|-----------|-------------|
| Esc       |             |
| Backspace |             |


## Description of some mechanics

---

### Using randomness

This mechanic has been added to increase the unpredictability of the behavior of the following game elements:
- the location of the stars in the sky (changes after each restart of the game);
```python
    star.x = randint(0, star.rect.width * 3) + randint(100, 250) * star_number
    star.rect.x = star.x

    star.y = randint(0, star.rect.height * 4) + randint(130, 200) * row_number
    star.rect.y = star.y
```
- selection of boosted alien ships (changes with each level);
```python
    index_boosted_aliens = random.sample(range(number_aliens_x*number_rows_aliens), count_boosted_aliens)
```
- selection of shooting alien ships (changes cyclically every N seconds).
```python
    shooting_aliens = random.sample(aliens.sprites(), num_shooting_aliens)
```

### The explosion of an air bomb in a certain radius
To find out how many aliens were in the radius of the bomb explosion, a formula is used to calculate the distance
between two points: the center of the bomb at the time of the explosion and the centers of all surviving aliens.

The formula looks like this:

<img src="images/formula.jpg" alt="Описание изображения" width="300" height="70"/>

```python
distance = math.sqrt((alien_center_x - explosion_center_x) ** 2 + (alien_center_y - explosion_center_y) ** 2)
        if distance < ai_settings.air_bomb_radius_explosion:
            destroyed_aliens.append(alien)
```

### Building an alien fleet
The formation of an alien fleet resembles the process of creating stars in the sky. However, unlike them, the 
coordinates of the location of the ships are clearly defined and do not depend on chance.

```python
    alien.x = alien_width / 2 + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    
    alien.y = alien_height/2 + 1.5 * alien_height * row_number
    alien.rect.y = alien.y
```

### Hit points of the boosted alien

### Background gradient

### Enhanced Player's Bullet

### The explosion effect

### The effect of the shot

### The effect of star movement

### The movement of the alien fleet



## Setting up the game

___
## Using tools

---
### Programming language 
### Libraries
### Development environment
### Music 
### Graphics



## Feedback

---