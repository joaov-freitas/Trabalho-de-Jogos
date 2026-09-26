from bullet import PlayerBullet, EnemyBullet
from enemy import Enemy

def singleton(class_):
    instances = { }

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)	
        return instances[class_]
    return getinstance

@singleton
class Collider ():
    def check_collisions(self,objects,player):

        player_bullets = [
            obj for obj in objects
            if isinstance(obj, PlayerBullet)
        ]

        enemy_bullets = [
            obj for obj in objects
            if isinstance(obj, EnemyBullet)
        ]

        enemies = [
            obj for obj in objects
            if isinstance(obj, Enemy)
        ]

        # PlayerBullet x Enemy
        for bullet in player_bullets:
            if bullet.impacting:
                continue # não colide se estiver impactando

            for enemy in enemies:

                if self.mask_collision(bullet, enemy):
                    enemy.hit()
                    bullet.hit()
                    break

        # EnemyBullet x Player
        for bullet in enemy_bullets:

            if self.mask_collision(bullet, player):
                player.hit()
                bullet.hit()
                break

    def mask_collision(self,obj1, obj2):
        rect1 = obj1.get_rect()
        rect2 = obj2.get_rect()

        if not rect1.colliderect(rect2):
            return False
        
        mask1 = obj1.get_mask()
        mask2 = obj2.get_mask()

        offset = (int(rect2.x - rect1.x), int(rect2.y - rect1.y))

        return mask1.overlap(mask2, offset) is not None