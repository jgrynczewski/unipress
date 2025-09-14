# Jump Sky Game - Difficulty Level Guide

This file documents the exact statistics and balance parameters for each difficulty level in the Jump Sky game.

## Difficulty Scaling System (1-10)

### Base Settings
- **Base Spawn Interval**: 3.0 seconds
- **Base Bird-to-Fruit Ratio**: 0.25 (1 bird per 4 fruits)
- **Base Max Objects**: 4 simultaneous
- **Base Safe Zone Duration**: 15.0 seconds
- **Base Safe Zone Cooldown**: 30.0 seconds
- **Base Object Speed**: 200 pixels/second

---

## Per-Difficulty Statistics

| Level | Spawn Interval | Bird Ratio | Max Objects | Safe Duration | Safe Cooldown | Jump Height | Speed Multi |
|-------|---------------|------------|-------------|---------------|---------------|-------------|-------------|
| 1     | 3.60s         | 0.125      | 4           | 22.50s        | 24.00s        | 270px       | 1.0x        |
| 2     | 3.56s         | 0.132      | 4           | 21.75s        | 24.96s        | 260px       | 1.1x        |
| 3     | 3.52s         | 0.138      | 4           | 21.00s        | 25.92s        | 250px       | 1.2x        |
| 4     | 3.48s         | 0.144      | 5           | 20.25s        | 26.88s        | 240px       | 1.3x        |
| 5     | 3.44s         | 0.150      | 5           | 19.50s        | 27.84s        | 230px       | 1.4x        |
| 6     | 3.40s         | 0.156      | 5           | 18.75s        | 28.80s        | 220px       | 1.5x        |
| 7     | 3.36s         | 0.162      | 6           | 18.00s        | 29.76s        | 210px       | 1.6x        |
| 8     | 3.32s         | 0.168      | 6           | 17.25s        | 30.72s        | 200px       | 1.7x        |
| 9     | 3.28s         | 0.174      | 6           | 16.50s        | 31.68s        | 190px       | 1.8x        |
| 10    | 3.24s         | 0.180      | 7           | 15.75s        | 32.64s        | 180px       | 1.9x        |

---

## Scaling Formulas

### Spawn Rate Scaling
```
difficulty_spawn_multiplier = 1.2 - (difficulty - 1) * 0.02
spawn_interval = base_spawn_interval * difficulty_spawn_multiplier
```
- **Range**: 1.2x (easy) to 1.02x (hard) of base interval
- **Result**: Easier = slower spawning, Harder = faster spawning

### Bird-to-Fruit Ratio Scaling  
```
difficulty_bird_multiplier = 0.5 + (difficulty - 1) * 0.06
bird_ratio = base_bird_ratio * difficulty_bird_multiplier
```
- **Range**: 0.5x (easy) to 1.04x (hard) of base ratio
- **Result**: Easier = fewer birds, Harder = more birds

### Max Objects Scaling
```
difficulty_objects_bonus = (difficulty - 1) // 3
max_objects = base_max_objects + difficulty_objects_bonus
```
- **Progression**: +1 object every 3 difficulty levels
- **Result**: More simultaneous challenge on higher difficulties

### Safe Zone Duration Scaling
```
difficulty_safe_multiplier = 1.5 - (difficulty - 1) * 0.05
safe_zone_duration = base_safe_duration * difficulty_safe_multiplier
```
- **Range**: 1.5x (easy) to 1.05x (hard) of base duration
- **Result**: Easier = longer safe zones, Harder = shorter safe zones

### Safe Zone Cooldown Scaling
```
difficulty_cooldown_multiplier = 0.8 + (difficulty - 1) * 0.04
safe_zone_cooldown = base_safe_cooldown * difficulty_cooldown_multiplier
```
- **Range**: 0.8x (easy) to 1.16x (hard) of base cooldown  
- **Result**: Easier = more frequent safe zones, Harder = less frequent

### Jump Height Scaling
```
difficulty_bonus = (11 - difficulty) * 10
desired_jump_height = base_jump_height + difficulty_bonus
```
- **Range**: +100px (easy) to +10px (hard) above base height
- **Result**: Easier = higher jumps for clearance, Harder = precise timing required

### Speed Scaling (All Objects)
```
difficulty_speed_multiplier = 1.0 + (difficulty - 1) * 0.1
final_velocity = base_object_speed * velocity_multiplier * difficulty_speed_multiplier
```
- **Range**: 1.0x (easy) to 1.9x (hard) speed multiplier
- **Result**: All objects move faster on higher difficulties

---

## Difficulty Profiles

### **Beginner (1-3)**: Learning Mode
- Slow, predictable spawning
- Minimal bird threats  
- Long, frequent safe zones
- High jumps for easy clearance
- Forgiving timing windows

### **Intermediate (4-6)**: Balanced Challenge
- Moderate spawn rates
- Balanced bird-to-fruit ratio
- Standard safe zone frequency
- Medium jump heights
- Requires strategic timing

### **Advanced (7-9)**: Skilled Players
- Fast spawning with more objects
- Increased bird frequency
- Shorter, less frequent safe zones
- Lower jumps requiring precision
- Multiple simultaneous threats

### **Expert (10)**: Maximum Challenge  
- Fastest spawn rates
- Highest bird density
- Minimal safe zone relief
- Lowest jumps with fastest speeds
- Constant decision-making required

---

## Usage for Balancing

When adjusting difficulty:

1. **Too Easy**: Increase bird ratio, decrease safe zone duration, reduce jump height
2. **Too Hard**: Decrease spawn rate, increase safe zone frequency, boost jump height  
3. **Boring**: Add more max objects, reduce safe zone cooldown
4. **Overwhelming**: Increase spawn interval, extend safe zone duration

## Version History

- **v1.0**: Initial comprehensive difficulty scaling system implemented
- **Last Updated**: Current session - Phase 2 polish-001 completion