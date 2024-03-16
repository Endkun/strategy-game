"""        update味方
        　　索敵
            行動をリセット
            　動くや攻撃などが次のターンまで続かないように、
        　　　イベントをisnotpushed(未操作状態)にする
                ステータスを"動く"にする
                イベント
                    (あらかじめcircleが
                　　索敵して相手が上下左右にいないか調べる
                　    範囲(●)を表示)
            　  索敵で縮められた範囲で動く
                　動いた(動いてない時も含む)時に範囲内に敵がいる場合●を押すと攻撃する
                if "migi" in self.enemyMove:
                    self.x += 1
                    self.energy -= 1
                    
                if "hidari" in self.enemyMove:
                    self.x -= 1
                    self.energy -= 1
                if "sita" in self.enemyMove:
                    self.y += 1
                    self.energy -= 1
                if "ue" in self.enemyMove:
                    self.y -= 1
                    self.energy -= 1
                print(self.name,self.energy)#-2になる。
                print(self.enemyMove)
                #ターン攻撃
                if "migi" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if "hidari" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if "sita" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if "ue" in self.enemyFight:
                    self.hp -= character.hp
                    self.energy -= 1
                    print(self.name,"は",character.name,"に攻撃した！")
                if self.energy <= 0:
                    Character.num += 1
                    self.energy = self.tenergy"""