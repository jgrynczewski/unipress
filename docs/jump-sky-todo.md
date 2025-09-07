# Jump Sky Game - Implementation Todo List

**Status**: Implementation Phase  
**Total Tasks**: 55  
**Current Phase**: Phase 1 - Core Mechanics

---

## Phase 1: Core Mechanics (High Priority)

### Setup & Project Structure
- [ ] **setup-001**: Create jump_sky project directory structure (games/jump_sky/, __init__.py, game.py, settings.toml)
- [ ] **setup-002**: Create asset directory structure (assets/images/games/jump_sky/{birds,fruits}, assets/sounds/games/jump_sky/)
- [ ] **setup-003**: Create localization files structure (locales/{pl_PL,en_US}/games/jump_sky.json)

### Git Flow & Configuration
- [ ] **git-001**: Follow Git Flow: switch to master, pull latest, create feat/jump-sky-game branch
- [ ] **config-001**: Create jump_sky settings.toml with essential configuration (physics, spawn, velocity, height, scoring)

### Base Game Implementation
- [ ] **base-001**: Create basic JumpSkyGame class inheriting from BaseGame with constructor and initial setup
- [ ] **physics-001**: Copy and adapt player physics from jumper game (gravity, jump mechanics, movement)

### Visual Fallback Systems
- [ ] **fallback-001**: Implement visual fallback system for fruits (apple=green circle+red border, banana=yellow crescent, pineapple=orange diamond, orange=orange circle)
- [ ] **fallback-002**: Implement visual fallback system for birds (3 colored triangles: red, blue, purple with simple rotation animation)
- [ ] **fallback-003**: Implement visual fallback system for player (blue rectangle with simple leg animation)
- [ ] **fallback-004**: Implement visual fallback system for background layers (gradient sky, gray triangular mountains, green tree rectangles, brown ground)

### Core Game Classes
- [ ] **classes-001**: Create Fruit class with properties: fruit_type, points, velocity, position, fallback_shape
- [ ] **classes-002**: Create Bird class with properties: bird_type, velocity, position, animation_frame, fallback_shape

### Velocity Systems
- [ ] **velocity-001**: Implement fruit velocity system based on point values (apple=1.0x, banana=1.3x, pineapple=1.6x, orange=2.0x)
- [ ] **velocity-002**: Implement bird velocity randomization system (0.8x to 1.8x multiplier per spawn)
- [ ] **velocity-003**: Integrate velocity system with difficulty scaling (base speed affected by difficulty 1-10)

### Spawn Systems
- [ ] **spawn-001**: Implement basic spawn system with 1 bird per 4 fruits ratio (bird_to_fruit_ratio = 0.25)
- [ ] **spawn-002**: Implement height randomization for objects (both birds and fruits: 60-150 pixels above ground)
- [ ] **spawn-003**: Implement maximum 4 simultaneous objects constraint
- [ ] **spawn-004**: Implement safe zones (periods with only fruits, no birds)
- [ ] **spawn-005**: Implement random bird type selection (bird1, bird2, bird3) per spawn

### Collision Detection
- [ ] **collision-001**: Implement fruit collision detection (throughout jump arc, fruit disappears, add points)
- [ ] **collision-002**: Implement bird collision detection (only when jumping, lose life, higher Z-order priority)
- [ ] **collision-003**: Implement collision priority system (bird collision overrides fruit collision)

### Scoring & Lives System
- [ ] **scoring-001**: Implement scoring system (apple=10, banana=15, pineapple=20, orange=25 points)
- [ ] **scoring-002**: Implement score display UI (integrate with BaseGame UI system)
- [ ] **lives-001**: Integrate standard 3-lives system from BaseGame (bird collision triggers life loss)
- [ ] **lives-002**: Implement pause-after-death mechanics (player blinking, click to continue)

### Audio & Internationalization
- [ ] **audio-001**: Implement basic audio system with silent fallback (no crash if sounds missing)
- [ ] **audio-002**: Define sound events: fruit_catch, bird_touched, jump, game_start, high_score
- [ ] **i18n-001**: Create basic Polish localization messages (ui.score, ui.lives, ui.game_over, ui.instructions)
- [ ] **i18n-002**: Create basic English fallback localization messages

### Phase 1 Testing & QA
- [ ] **test-001**: Test Phase 1: Basic gameplay with fallback visuals works correctly
- [ ] **test-002**: Test Phase 1: Verify fruit collection scoring and bird collision life loss
- [ ] **test-003**: Test Phase 1: Verify spawn ratio approximately 1 bird per 4 fruits
- [ ] **test-004**: Test Phase 1: Verify velocity differences visible (higher-value fruits faster, birds random speeds)
- [ ] **test-005**: Test Phase 1: Verify different bird types spawn randomly (different colored triangles)
- [ ] **test-006**: Test Phase 1: Verify fallback visual system works (recognizable shapes, animated birds)
- [ ] **qa-001**: Run quality checks: ruff check && ruff format && mypy unipress

---

## Phase 2: Assets & Polish (Medium Priority)

### Asset Requests
- [ ] **assets-001**: Request user assets: bird animations (3 types, 4 frames each in birds/{bird1,bird2,bird3}/ folders)
- [ ] **assets-002**: Request user assets: fruit images (apple.png, banana.png, pineapple.png, orange.png in fruits/ folder)
- [ ] **assets-003**: Request user assets: sound files (jump.ogg, success.ogg, failure.ogg, game_start.ogg, high_score.ogg)

### Asset Integration
- [ ] **integration-001**: Copy player assets from jumper game to jump_sky (or use fallback if copying fails)
- [ ] **integration-002**: Replace fruit fallbacks with user-provided images (when available)
- [ ] **integration-003**: Replace bird fallbacks with user-provided animations (when available)
- [ ] **integration-004**: Integrate user-provided sound files with audio system (when available)
- [ ] **integration-005**: Create animation metadata files for bird animations (JSON format)

### Polish & Balance
- [ ] **polish-001**: Fine-tune spawn rates and gameplay balance across difficulty levels 1-10
- [ ] **polish-002**: Implement proper UI feedback and visual polish
- [ ] **polish-003**: Integrate with end game screen (Play Again/Exit cycling buttons)
- [ ] **polish-004**: Integrate with high score system (persistent JSON storage)

### Phase 2 Testing
- [ ] **test-phase2-001**: Test Phase 2: All assets display correctly with proper animations
- [ ] **test-phase2-002**: Test Phase 2: Sound events trigger at appropriate times
- [ ] **test-phase2-003**: Test Phase 2: Professional visual and audio feedback works

---

## Phase 3: Final Integration & Testing (Medium Priority)

### Comprehensive Testing
- [ ] **final-001**: Comprehensive testing across all difficulty levels (1-10) for balanced gameplay
- [ ] **final-002**: Performance testing with maximum objects (4 simultaneous) - verify 60+ FPS
- [ ] **final-003**: Cross-platform compatibility testing (including Docker containers)
- [ ] **final-004**: Integration testing with existing Unipress framework (BaseGame, settings, i18n, sounds)

### Final Quality Assurance
- [ ] **final-005**: Final quality assurance: run full test suite and all quality checks

---

## Project Completion (Low Priority)

### Documentation & Release
- [ ] **completion-001**: Update documentation and plan status to completed
- [ ] **completion-002**: Create pull request for jump_sky game implementation
- [ ] **completion-003**: Update CHANGELOG.md with new jump_sky game addition

---

## Progress Tracking

### Phase 1 Progress: 0/33 tasks completed (0%)
- [ ] Setup & Structure: 0/3
- [ ] Git Flow & Config: 0/2  
- [ ] Base Implementation: 0/2
- [ ] Fallback Systems: 0/4
- [ ] Core Classes: 0/2
- [ ] Velocity Systems: 0/3
- [ ] Spawn Systems: 0/5
- [ ] Collision Detection: 0/3
- [ ] Scoring & Lives: 0/4
- [ ] Audio & i18n: 0/4
- [ ] Testing & QA: 0/7

### Phase 2 Progress: 0/14 tasks completed (0%)
- [ ] Asset Requests: 0/3
- [ ] Asset Integration: 0/5
- [ ] Polish & Balance: 0/4
- [ ] Phase 2 Testing: 0/3

### Phase 3 Progress: 0/5 tasks completed (0%)
- [ ] Testing: 0/4
- [ ] Final QA: 0/1

### Completion Progress: 0/3 tasks completed (0%)

**Overall Progress: 0/55 tasks completed (0%)**

---

## Development Requirements & Workflow

### Commit & PR Requirements
1. **Separate Commits**: Each significant feature/task must be committed separately with proper git-cz format
2. **Pull Requests**: Create MR/PR for every completed significant task for review
3. **Commit Messages**: Follow conventional format: `feat: 🎸 add basic JumpSkyGame class`
4. **Atomic Changes**: One logical change per commit, never bundle unrelated fixes
5. **Clean Commit Messages**: NEVER include "Generated with Claude Code" or "Co-Authored-By: Claude" lines in commit messages

### Manual Testing Requirements
After completing each significant task, the developer must:
1. **Provide Testing Instructions**: Include specific step-by-step instructions for user verification
2. **User Verification Required**: User must manually test and confirm functionality works correctly
3. **Testing Commands**: Specify exact commands to run the test (e.g., `uv run python -m unipress.games.jump_sky.game 5`)
4. **Expected Behavior**: Clearly describe what should happen during the test
5. **Success Criteria**: Define clear pass/fail criteria for the test

### Significant Tasks Requiring Manual Testing
- **setup-001** through **setup-003**: Directory structure verification
- **base-001**: Basic game class functionality
- **physics-001**: Player physics and movement
- **fallback-001** through **fallback-004**: Visual fallback systems
- **classes-001** through **classes-002**: Core game objects
- **collision-001** through **collision-003**: Collision detection systems
- **scoring-001** through **scoring-002**: Scoring system
- **spawn-001** through **spawn-005**: Object spawning mechanics
- All **test-*** tasks: Comprehensive gameplay verification

---

## Usage Instructions

1. **Start with Phase 1**: Complete all high-priority tasks first
2. **Mark Completed Tasks**: Change `- [ ]` to `- [x]` when task is done
3. **Update Progress Counters**: Update the progress tracking section
4. **Sequential Execution**: Follow task order for dependencies
5. **Testing Milestones**: Don't skip testing tasks - they verify each phase works
6. **Commit After Each Task**: Create separate commits for significant completed tasks
7. **Request User Testing**: Provide testing instructions and wait for user verification

## Next Task
**Current**: setup-001 - Create jump_sky project directory structure

Ready to begin implementation!