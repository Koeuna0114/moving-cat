"""
🐱 고양이 장애물 피하기 - 리얼타임 게임! 🐱
- 자동으로 내려오는 장애물을 실시간으로 피하세요!
"""

import random
import time
import threading
import sys

class CatDodgeGame:
    """자동 움직이는 장애물 게임"""
    
    def __init__(self, width=12, height=8):
        self.width = width
        self.height = height
        self.cat_pos = width // 2
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.target_score = 15
        self.frame = 0
        
    def show_tutorial(self):
        """게임 설명"""
        print("\n" + "=" * 50)
        print("🐱 고양이 장애물 피하기 - 리얼타임 버전!")
        print("=" * 50)
        print("\n[게임 규칙]")
        print("✓ 장애물이 자동으로 내려옵니다! (입력 기다리지 않음)")
        print("✓ 15개를 피하면 승리!")
        print("✓ 한 번 부딪히면 게임오버!")
        print("\n[조작 방법]")
        print("  👈  'a' 입력 = 왼쪽으로 이동")
        print("  👉  'd' 입력 = 오른쪽으로 이동")
        print("  ⏸   'q' 입력 = 게임 종료")
        print("\n[난이도]")
        print("  ▪️ 보드: 12 x 8 (매우 좁음)")
        print("  ▪️ 속도: 자동으로 빠르게")
        print("  ▪️ 다중 장애물: 동시 출현")
        print("\n" + "=" * 50)
        input("▶ 준비 되셨으면 엔터를 누르세요! ")
        
    def draw(self):
        """게임 화면 출력"""
        # 화면 초기화
        print("\033[H\033[J", end="")
        
        # 보드 생성
        board = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # 장애물 그리기
        for obs_x, obs_y in self.obstacles:
            if 0 <= obs_y < self.height and 0 <= obs_x < self.width:
                board[obs_y][obs_x] = '#'
        
        # 고양이 그리기
        if 0 <= self.cat_pos < self.width:
            board[self.height - 1][self.cat_pos] = '🐱'
        
        # 화면 출력
        print("=" * (self.width + 2))
        for row in board:
            print("|" + "".join(row) + "|")
        print("=" * (self.width + 2))
        print(f"점수: {self.score}/{self.target_score} | 남은 피할 횟수: {self.target_score - self.score}")
        print("조작: 'a'(좌) 'd'(우) 'q'(종료)")
        
    def move_cat(self, direction):
        """고양이 이동"""
        new_pos = self.cat_pos + direction
        if 0 <= new_pos < self.width:
            self.cat_pos = new_pos
    
    def input_loop(self):
        """입력 처리 스레드"""
        while not self.game_over:
            try:
                user_input = input().lower().strip()
                
                if user_input == 'q':
                    self.game_over = True
                elif user_input == 'a':
                    self.move_cat(-1)
                elif user_input == 'd':
                    self.move_cat(1)
            except (EOFError, KeyboardInterrupt):
                self.game_over = True
                break
            
    def game_loop(self):
        """백그라운드 게임 루프 - 자동으로 장애물 이동"""
        while not self.game_over:
            time.sleep(0.6)  # 0.6초마다 업데이트 (느림)
            
            self.frame += 1
            
            # 매 2프레임마다 새 장애물 생성
            if self.frame % 2 == 0:
                num = random.randint(1, 2)
                for _ in range(num):
                    self.obstacles.append([
                        random.randint(0, self.width - 1),
                        0
                    ])
            
            # 모든 장애물을 아래로 이동
            new_obstacles = []
            for obs in self.obstacles:
                obs[1] += 1
                
                # 고양이와 충돌 검사
                if obs[1] == self.height - 1 and obs[0] == self.cat_pos:
                    self.game_over = True
                    break
                
                # 화면 내 장애물 유지
                if obs[1] < self.height:
                    new_obstacles.append(obs)
                else:
                    # 화면 아래로 나감 = 피함!
                    self.score += 1
                    if self.score >= self.target_score:
                        self.game_over = True
            
            self.obstacles = new_obstacles
        
    def run(self):
        """게임 시작"""
        self.show_tutorial()
        
        # 백그라운드 게임 루프 시작
        game_thread = threading.Thread(target=self.game_loop, daemon=True)
        game_thread.start()
        
        # 입력 스레드 시작
        input_thread = threading.Thread(target=self.input_loop, daemon=True)
        input_thread.start()
        
        print("\n🎮 게임 시작! 빠르게 반응하세요!\n")
        time.sleep(0.5)
        
        # 메인 스레드: 계속 화면 업데이트
        while not self.game_over:
            self.draw()
            time.sleep(0.1)  # 0.1초마다 화면 갱신
        
        # 게임 종료 화면
        time.sleep(0.5)
        self.draw()
        print("\n" + "=" * 50)
        
        if self.score >= self.target_score:
            print("🏆 축하합니다! 승리했습니다!")
            print(f"점수: {self.score}/{self.target_score}")
        else:
            print("💥 게임 오버!")
            print(f"점수: {self.score}/{self.target_score}")
        print("=" * 50)


if __name__ == "__main__":
    game = CatDodgeGame()
    game.run() 
