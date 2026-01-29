#!/usr/bin/env python3
"""
Script to create high score saving functionality for games
"""
import json
import os

class HighScoreManager:
    """Manages persistent high scores for games"""
    
    def __init__(self, save_file="high_scores.json"):
        self.save_file = save_file
        self.scores = self.load_scores()
    
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        
        # Return default scores if file doesn't exist or is corrupted
        return {
            "void_drift": 0,
            "brickfall": 0
        }
    
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def get_high_score(self, game_name):
        """Get high score for a specific game"""
        return self.scores.get(game_name, 0)
    
    def update_high_score(self, game_name, new_score):
        """Update high score for a specific game"""
        current_high = self.get_high_score(game_name)
        if new_score > current_high:
            self.scores[game_name] = new_score
            self.save_scores()
            return True
        return False
    
    def reset_high_score(self, game_name):
        """Reset high score for a specific game"""
        self.scores[game_name] = 0
        self.save_scores()

# Test the high score manager
if __name__ == "__main__":
    manager = HighScoreManager()
    
    # Test saving and loading
    print("Testing high score manager...")
    print(f"Void Drift High Score: {manager.get_high_score('void_drift')}")
    print(f"Brickfall High Score: {manager.get_high_score('brickfall')}")
    
    # Test updating
    manager.update_high_score('void_drift', 1000)
    manager.update_high_score('brickfall', 500)
    
    print(f"Updated Void Drift High Score: {manager.get_high_score('void_drift')}")
    print(f"Updated Brickfall High Score: {manager.get_high_score('brickfall')}")
    
    print("High score manager test completed!")