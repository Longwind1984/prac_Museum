# Agent 状态机形式化（XState）

> 这份文档把 [Agent 体验设计 v0 §4.3](./agent-experience.md) 的选模式决策树形式化为 XState 风格的状态机定义，机器可读、可可视化、可作为 Figma 信息架构的输入。
>
> XState 选型理由：(1) 业界事实标准的 statecharts 实现；(2) JSON 可序列化，可被 stately.ai/viz 直接渲染；(3) 表达 parallel states 自然，正好对应本产品 spatial / audio / fatigue / memory 四个并行状态域。

---

## 0. 文档信息

| 字段 | 值 |
| --- | --- |
| 文档版本 | v0 |
| 文档日期 | 2026-05-17 |
| 关联 | [Agent 体验设计 v0](./agent-experience.md) §4.3、PRD §7.4 |

---

## 1. 顶层结构

```
museumAgent (root, type=parallel)
│
├── spatial            ← 主线：物理位置驱动的模式调度
│   ├── outside ⟵ initial
│   ├── enteringHall
│   ├── inHall
│   │   ├── idle ⟵ initial
│   │   ├── atArtifact
│   │   ├── closePhone
│   │   └── onBreak
│   ├── leaving
│   └── afterVisit
│
├── audio              ← 并行：音频路由
│   ├── speaker ⟵ initial
│   └── earphone
│
├── fatigue            ← 并行：疲倦累积
│   ├── fresh ⟵ initial
│   ├── mid
│   └── tired
│
├── memory             ← 并行：当前文物的跨次记忆状态
│   ├── cold ⟵ initial
│   └── warm
│
└── promise            ← 并行：长程承诺队列（context-only，无状态分支）
```

四个并行域同时活跃。spatial 是主线，其余三个为它提供 guard 数据。

---

## 2. Context（扩展状态）

```typescript
interface AgentContext {
  // spatial
  location: 'Outside' | { hall: string };
  currentArtifact: ArtifactId | null;
  dwellStartedAt: Date | null;
  dwellBucket: 'none' | 'short' | 'mid' | 'long' | 'lingering';

  // memory
  memoryMatches: MemoryMatch[];          // 当前文物的潜在 wow 触发匹配
  matchCooldowns: Map<ArtifactId, Date>; // 24h 冷却表

  // promise queue
  promiseQueue: Promise[];

  // 主动性预算
  aiInitiateCountToday: number;
  userInitiateCountToday: number;
  lastAiInitiateAt: Date | null;

  // 用户意图
  mainIntent: 'ACTIVE' | 'CASUAL';       // T1 选「嗯」/「随便看看」结果

  // session
  sessionStartedAt: Date;
  artifactsSeen: { artifact: ArtifactId; dwell: number; userInputs: string[] }[];
  papersSavedTonight: PaperId[];

  // returning user
  priorVisitsToCurrentHall: number;
  lastVisitToCurrentHall: Date | null;
}

interface MemoryMatch {
  matchedArtifact: { id; museum; visitedAt; dwell; userQuotesThen };
  similarityScore: number;
  similarityType: 'style_lineage' | 'dwell_correspondence' | 'user_phrase_recall';
}

interface Promise {
  id: string;
  madeAt: Date;
  topic: string;
  fulfillWhen: { type: 'spatial'; condition: string } | { type: 'temporal'; condition: string };
  fulfillPattern: 'M-02-comparison-variant' | 'M-07' | 'memory-card-only';
  expiresAfterVisit: boolean;
}
```

---

## 3. Event Catalog

| Event | 来源 | Payload |
| --- | --- | --- |
| `LOCATION_CHANGE` | BLE 信标 / GPS | `{from: Location, to: Location}` |
| `ARRIVE_AT_ARTIFACT` | BLE 微信标 / 加速度计 | `{artifactId}` |
| `DEPART_FROM_ARTIFACT` | 加速度计 / 信标 | `{artifactId, dwell}` |
| `DWELL_TICK` | 内部 5s 定时器 | `{dwell, dwellBucket}` |
| `USER_INPUT` | UI | `{type: 'text'|'voice'|'emoji', value}` |
| `PICKUP_GESTURE` | 加速度计 | `{}` |
| `WIDGET_TAP` | 锁屏 widget | `{}` |
| `USER_TAP_WELCOME` | 欢迎卡 | `{intent: 'ACTIVE'|'CASUAL'}` |
| `USER_TAP_MY_VIEW` | 卡片标签 | `{}` |
| `CLOSE_PHONE_BUTTON_PRESS` | 卡片按钮 | `{}` |
| `CLOSE_PHONE_TIMEOUT` | 30s 倒计时结束 | `{}` |
| `CLOSE_PHONE_LONG_PRESS_EXIT` | 长按 3s | `{}` |
| `EARPHONE_CONNECT` | 系统 audio route | `{}` |
| `EARPHONE_DISCONNECT` | 系统 audio route | `{}` |
| `NOISY_ENV_DETECTED` | 麦克风分贝 | `{db: number}` |
| `FATIGUE_TICK` | 内部 1min 定时器 | `{}` |
| `MEMORY_FETCH_RESPONSE` | RAG 异步回调 | `{matches: MemoryMatch[]}` |
| `PROMISE_FULFILL_CHECK_TICK` | 内部 5s 定时器 | `{}` |
| `LEAVE_HALL` | BLE 信标 | `{lastHall}` |
| `LEAVING_CONFIRMED` | 5min 后仍在 Outside | `{}` |
| `RETURN_TO_HALL` | 5min 内回到任意 Hall | `{}` |
| `OPEN_APP_LATER` | 离馆后 App 启动 | `{}` |
| `USER_ADD_THOUGHT` | 离馆后输入补充 | `{artifactId, thought}` |

---

## 4. Guard Catalog

```typescript
const guards = {
  // M-04 主动开口的核心门槛
  shouldInitiateFromMemory: (ctx, event) =>
    ctx.memoryMatches.length >= 1
      && ctx.memoryMatches[0].similarityScore >= 0.75
      && ctx.dwellBucket in ['mid', 'long', 'lingering']
      && !isNoisySpeaker(ctx)
      && minutesSince(ctx.lastAiInitiateAt) >= 15
      && (ctx.userInitiateCountToday / Math.max(1, ctx.aiInitiateCountToday)) >= 2.0
      && !ctx.matchCooldowns.has(ctx.memoryMatches[0].matchedArtifact.id),

  // M-03 承诺兑现
  hasReadyPromise: (ctx) =>
    ctx.promiseQueue.some(p => evalFulfillCondition(p.fulfillWhen, ctx)),

  // 用户问题类型分类（给 dispatchPattern 用）
  isCrossArtifactQuestion: (_, event) =>
    semanticMatch(event.value, ['区别', '演变', '谱系', '为什么', '比起', '跟.*不一样']),

  isDatingQuestion: (_, event) =>
    semanticMatch(event.value, ['什么时期', '朝代', '几世纪', '应该是.*的', '风格', '工坊']),

  isFirstInputOnArtifact: (ctx) =>
    !ctx.artifactsSeen.find(a => a.artifact === ctx.currentArtifact && a.userInputs.length > 0),

  // 疲倦累积
  shortDwellsAccumulating: (ctx) =>
    last(5, ctx.artifactsSeen).every(a => a.dwell < 30),

  persistentShortDwell: (ctx) =>
    last(10, ctx.artifactsSeen).filter(a => a.dwell < 30).length >= 8,

  // 噪声环境
  isNoisySpeaker: (ctx) =>
    ctx.audio === 'speaker' && ctx.noiseDb > 70,

  // 主动性预算
  underInitiateRateCeiling: (ctx) =>
    (ctx.aiInitiateCountToday / Math.max(1, ctx.userInitiateCountToday)) <= 0.5,
};
```

---

## 5. Action Catalog

```typescript
const actions = {
  // pattern dispatchers
  triggerM01: 'dispatchPattern(M-01, currentContext)',
  triggerM02: 'dispatchPattern(M-02, currentContext)',
  triggerM03Create: 'dispatchPattern(M-03, currentContext) + createPromise',
  triggerM03Fulfill: 'dispatchPattern(M-03-fulfill, readyPromise)',
  triggerM04: 'dispatchPattern(M-04, currentContext) + incrementAiInitiate + setMatchCooldown(24h)',
  triggerM05Phase1: 'blackOutScreen + startCountdown(30s)',
  triggerM05Phase2: 'dispatchPattern(M-05-phase2, currentContext)',
  triggerM06: 'dispatchPattern(M-06, currentContext)',
  triggerM07: 'dispatchPattern(M-07, currentContext) + maybeSavePaper',
  triggerM08: 'dispatchPattern(M-08, sessionState)',
  triggerM08AddThought: 'dispatchPattern(M-08-addThought, userAddition) + writeToLongTermMemory',

  // state updates
  setCurrentArtifact: 'assign({ currentArtifact: event.artifactId, dwellStartedAt: Date.now() })',
  startDwellTimer: 'schedule(DWELL_TICK, every: 5s)',
  recordArtifactSeen: 'assign({ artifactsSeen: [...prev, { artifact, dwell }] })',
  cacheMemoryMatches: 'assign({ memoryMatches: event.matches })',
  setMatchCooldown: 'assign({ matchCooldowns: prev.set(id, now + 24h) })',
  incrementAiInitiate: 'assign({ aiInitiateCountToday: prev + 1 })',
  incrementUserInitiate: 'assign({ userInitiateCountToday: prev + 1 })',

  // tool calls (async)
  eagerFetchHallContent: 'invokeService(ragFetchHall, hall: ctx.location.hall)',
  eagerFetchArtifact: 'invokeService(ragFetchArtifact, id: ctx.currentArtifact)',
  eagerFetchMemoryMatches: 'invokeService(memoryFetch, user, ctx.currentArtifact)',

  // audio
  switchToVoiceMode: 'shrinkScreenToReference + activateVoiceOut',
  switchToScreenMode: 'expandScreenToCard + deactivateVoiceOut',
  dimScreen: 'reduceBrightness(1 step)',

  // session
  startLeavingTimer: 'schedule(LEAVING_CONFIRMED, after: 5min)',
};
```

---

## 6. Spatial 主状态机

```typescript
const spatialMachine = {
  id: 'spatial',
  initial: 'outside',
  states: {

    outside: {
      on: {
        LOCATION_CHANGE: [
          {
            cond: 'isEnteringHall',
            target: 'enteringHall',
            actions: ['assignLocation']
          }
        ]
      }
    },

    enteringHall: {
      entry: ['triggerM01', 'eagerFetchHallContent'],
      on: {
        USER_TAP_WELCOME: {
          target: 'inHall',
          actions: ['assignMainIntent']
        },
        WIDGET_TAP: 'inHall',
        TIMEOUT_5MIN: 'inHall'  // 用户没响应，进入沉默 inHall
      }
    },

    inHall: {
      initial: 'idle',

      states: {

        idle: {
          on: {
            ARRIVE_AT_ARTIFACT: {
              target: 'atArtifact',
              actions: ['setCurrentArtifact', 'startDwellTimer', 'eagerFetchArtifact', 'eagerFetchMemoryMatches']
            }
          }
        },

        atArtifact: {
          on: {
            DEPART_FROM_ARTIFACT: {
              target: 'idle',
              actions: ['recordArtifactSeen']
            },

            USER_INPUT: [
              {
                cond: 'isCrossArtifactQuestion',
                actions: ['triggerM03Create', 'incrementUserInitiate']
              },
              {
                cond: 'isDatingQuestion AND ragHasDispute',
                actions: ['triggerM07', 'incrementUserInitiate']
              },
              {
                cond: 'isFirstInputOnArtifact',
                actions: ['triggerM02', 'incrementUserInitiate']
              },
              {
                // default: continued conversation, M-02 variant
                actions: ['triggerM02', 'incrementUserInitiate']
              }
            ],

            PICKUP_GESTURE: {
              actions: ['showLockScreenWidget']
            },

            USER_TAP_MY_VIEW: {
              actions: ['triggerM06']
            },

            CLOSE_PHONE_BUTTON_PRESS: 'closePhone',

            // M-04 主动开口（只在 DWELL_TICK 上检查）
            DWELL_TICK: [
              {
                cond: 'hasReadyPromise',
                actions: ['triggerM03Fulfill']
              },
              {
                cond: 'shouldInitiateFromMemory',
                actions: ['triggerM04']
              }
              // 默认：什么都不做 (SILENT)
            ],

            PROMISE_FULFILL_CHECK_TICK: [
              {
                cond: 'hasReadyPromise',
                actions: ['triggerM03Fulfill']
              }
            ]
          }
        },

        closePhone: {
          entry: ['triggerM05Phase1'],
          on: {
            CLOSE_PHONE_TIMEOUT: {
              target: 'atArtifact',
              actions: ['triggerM05Phase2']
            },
            CLOSE_PHONE_LONG_PRESS_EXIT: 'atArtifact'
          }
        },

        onBreak: {
          on: {
            RESUME_FROM_BREAK: 'idle'
          }
        }
      },

      on: {
        LEAVE_HALL: 'leaving',
        FATIGUE_TO_TIRED: { target: '.onBreak', actions: ['suggestBreak'] }
        // suggestBreak 是 M-08-precursor，不进入 leaving
      }
    },

    leaving: {
      entry: ['startLeavingTimer'],
      on: {
        LEAVING_CONFIRMED: {
          target: 'afterVisit',
          actions: ['triggerM08']
        },
        RETURN_TO_HALL: 'inHall.idle'  // 上厕所兜底
      }
    },

    afterVisit: {
      on: {
        OPEN_APP_LATER: {
          actions: ['renderMemoryCard']
        },
        USER_ADD_THOUGHT: {
          actions: ['triggerM08AddThought']
        }
      }
    }
  }
};
```

---

## 7. 并行子状态机

### 7.1 audio

```typescript
const audioMachine = {
  id: 'audio',
  initial: 'speaker',
  states: {
    speaker: {
      on: {
        EARPHONE_CONNECT: {
          target: 'earphone',
          actions: ['switchToVoiceMode']
        },
        NOISY_ENV_DETECTED: {
          // 不切换 audio，只 dimScreen——这是 PRD §7.2 T8 的硬约束
          actions: ['dimScreen']
        }
      }
    },
    earphone: {
      on: {
        EARPHONE_DISCONNECT: {
          target: 'speaker',
          actions: ['switchToScreenMode']
        }
      }
    }
  }
};
```

### 7.2 fatigue

```typescript
const fatigueMachine = {
  id: 'fatigue',
  initial: 'fresh',
  states: {
    fresh: {
      on: {
        FATIGUE_TICK: [
          { cond: 'shortDwellsAccumulating', target: 'mid' }
        ]
      }
    },
    mid: {
      on: {
        FATIGUE_TICK: [
          { cond: 'persistentShortDwell', target: 'tired' },
          { cond: 'dwellsRecovered', target: 'fresh' }
        ]
      }
    },
    tired: {
      // 进入 tired 即向 spatial 发送 FATIGUE_TO_TIRED 事件
      entry: ['raise:FATIGUE_TO_TIRED'],
      on: {
        REST_TAKEN: 'fresh'
      }
    }
  }
};
```

### 7.3 memory

```typescript
const memoryMachine = {
  id: 'memory',
  initial: 'cold',
  states: {
    cold: {
      on: {
        MEMORY_FETCH_RESPONSE: [
          {
            cond: 'matchesViable',
            target: 'warm',
            actions: ['cacheMemoryMatches']
          }
        ]
      }
    },
    warm: {
      on: {
        ARRIVE_AT_ARTIFACT: 'cold',         // 切换文物即重置
        DEPART_FROM_ARTIFACT: 'cold'
      }
    }
  }
};
```

### 7.4 promise (context-only sub-machine)

不需要状态分支——只是 context 中的队列。被 spatial 的 `hasReadyPromise` guard 查询，被 actions 修改。

---

## 8. 完整决策树（spatial.inHall.atArtifact 状态下的事件分派）

这是 §4.3 的形式化版本：

```
                          EVENT IN atArtifact
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   USER 事件                SYSTEM 事件               INTERNAL TICK
        │                        │                        │
        ├── USER_INPUT           ├── PICKUP_GESTURE       ├── DWELL_TICK
        │   │                    │   │                    │   │
        │   ├─ cross-artifact?   │   └→ showWidget        │   ├─ hasReadyPromise?
        │   │  YES → M-03 create │                        │   │  YES → M-03 fulfill
        │   │  NO ↓              ├── EARPHONE_CONNECT     │   │  NO ↓
        │   │                    │   └→ switchToVoice     │   │
        │   ├─ dating + dispute? │                        │   ├─ shouldInitiate-
        │   │  YES → M-07        ├── EARPHONE_DISCONNECT  │   │  FromMemory?
        │   │  NO ↓              │   └→ switchToScreen    │   │  YES → M-04
        │   │                    │                        │   │  NO ↓
        │   ├─ first input?      ├── NOISY_ENV            │   │
        │   │  YES → M-02        │   └→ dimScreen         │   └─ SILENT (default)
        │   │  NO ↓              │                        │
        │   │                    └── DEPART_FROM_ARTIFACT │
        │   └─ M-02 variant      │   └→ inHall.idle       └── PROMISE_FULFILL_TICK
        │                                                     │
        ├── USER_TAP_MY_VIEW                                  └─ similar to DWELL_TICK
        │   └→ M-06
        │
        └── CLOSE_PHONE_BUTTON_PRESS
            └→ inHall.closePhone (M-05 phase 1)
```

**关键性质**：DWELL_TICK 这条路径上有 ≥ 2 个 cond 不满足时，**默认行为是 SILENT**——不报错、不重试、不上 fallback。这是把"默认沉默"（PRD §6 第 5 条）落到状态机层。

---

## 9. Sample Event Trace

模拟 PRD §7.2 一日剧本的前 5 个触点：

```
TIMESTAMP   EVENT                         spatial               audio    fatigue  memory   ACTIONS
─────────────────────────────────────────────────────────────────────────────────────────────────────
14:00:00    INIT                          outside               speaker  fresh    cold     —
14:02:10    LOCATION_CHANGE(Out→Hall:佛)  outside               ─        ─        ─        assignLocation
                                          → enteringHall                                   triggerM01 (T1)
                                                                                            eagerFetchHallContent
14:02:13    [async] MEMORY_FETCH_RESP     enteringHall          ─        ─        cold     cacheMemoryMatches
                                          ─                                       → warm
14:02:30    USER_TAP_WELCOME({ACTIVE})    enteringHall          ─        ─        ─        assignMainIntent
                                          → inHall.idle
14:07:50    ARRIVE_AT_ARTIFACT(a-001)     inHall.idle           ─        ─        warm     setCurrentArtifact
                                          → inHall.atArtifact                              startDwellTimer
                                                                                            eagerFetchArtifact
                                                                                            (memory: a-001 has no match)
                                                                                            ↓ memory → cold
14:08:30    PICKUP_GESTURE                inHall.atArtifact     ─        ─        cold     showLockScreenWidget (T2)
14:08:40    WIDGET_TAP                    inHall.atArtifact     ─        ─        ─        openYourViewPicker
14:08:55    USER_INPUT({emoji:"庄严"})    inHall.atArtifact     ─        ─        ─        guard:isFirstInputOnArtifact ✓
                                                                                            triggerM02 (T3)
                                                                                            incrementUserInitiate
14:11:20    USER_INPUT("北魏早晚区别")    inHall.atArtifact     ─        ─        ─        guard:isCrossArtifactQuestion ✓
                                                                                            triggerM03Create (T4)
                                                                                            createPromise (a-014)
                                                                                            incrementUserInitiate
14:22:50    DEPART_FROM_ARTIFACT          inHall.atArtifact     ─        ─        ─        recordArtifactSeen
                                          → inHall.idle
14:22:55    ARRIVE_AT_ARTIFACT(a-005)     inHall.idle           ─        ─        cold     setCurrentArtifact
                                          → inHall.atArtifact                              eagerFetchMemoryMatches
14:22:58    [async] MEMORY_FETCH_RESP     inHall.atArtifact     ─        ─        cold     cacheMemoryMatches
                                                                                  → warm   (match: 国博 曹衣出水)
14:23:50    DWELL_TICK (dwell=55s,mid)    inHall.atArtifact     ─        ─        warm     guard:hasReadyPromise ✗
                                                                                            guard:shouldInitiateFrom
                                                                                              Memory ✓
                                                                                            triggerM04 (T5)
                                                                                            incrementAiInitiate
                                                                                            setMatchCooldown(国博曹衣出水, 24h)
```

可以直接喂给 stately.ai/viz 或 XState 内置 visualizer 渲染。

---

## 10. 给 Figma 信息架构的输入

把这份状态机翻译到 Figma 时：

1. **每一个 state 节点 = 一个/一组屏**。例如 `inHall.atArtifact` 不是单屏，是 "看文物时所有可能屏" 的容器；`inHall.closePhone` 是单屏（全黑 + 倒计时）。
2. **每一条 transition = 一条屏间连线**。在 Figma 上用箭头连接，箭头标签 = event name。
3. **每一个 action = 屏上发生什么**（trigger 哪个 pattern、调哪个工具）。
4. **每一个 guard = 屏间连线的条件标签**。
5. **并行子状态机** = 系统级 modifier（屏在 audio.earphone 状态下呈现耳机模式 / 在 fatigue.tired 状态下呈现休息建议）。

建议在 Figma 里用 4 层 frame：
- Layer 1：spatial state hierarchy（树状导航）
- Layer 2：每个 state 的 detail screen（一屏或一组）
- Layer 3：parallel modifier 叠加（音频 / 疲倦 / 记忆）
- Layer 4：模式触发的展开示例（M-04 wow 时刻、M-06 四卡）

---

## 11. 与 PRD §7.4 状态机的对齐

| PRD §7.4 维度 | 本文档对应 |
| --- | --- |
| `Location` | spatial 主状态机 + context.location |
| `Dwell` | context.dwellBucket，DWELL_TICK 更新 |
| `Audio` | audio 子状态机 |
| `Promise` | context.promiseQueue + PROMISE_FULFILL_CHECK_TICK |
| `Memory` | memory 子状态机 + context.memoryMatches |
| `Fatigue` | fatigue 子状态机 |

PRD §7.4.2 主动开口门槛函数 → 本文档 §4 `shouldInitiateFromMemory` guard
PRD §7.4.3 模式切换矩阵 → 本文档 §7.1 audio 子状态机
PRD §7.4.4 跨次记忆三类触发 → 本文档 `cacheMemoryMatches` action 处理
PRD §7.4.5 长程承诺 → 本文档 §3 Promise interface + §6 atArtifact 的 hasReadyPromise / triggerM03Fulfill

---

**[ v0 结束 ]**

下一步：把这份 XState spec 喂给 stately.ai/viz 渲染成可视化图，作为 Figma IA 工作的视觉参考。
