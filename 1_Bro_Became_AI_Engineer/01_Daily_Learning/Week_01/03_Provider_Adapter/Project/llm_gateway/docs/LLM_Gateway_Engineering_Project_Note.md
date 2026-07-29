# LLM Gateway
## Engineering Project Note

> **Invariant:** application use cases depend on an LLM contract, not on a provider SDK.
>
> **Pipeline:** **RECEIVE → CONFIGURE → RESOLVE → ADAPT → EXECUTE → RETURN**

---

# 1. Project Overview

LLM Gateway is a lightweight Python application that demonstrates the **Provider Adapter Pattern** for Large Language Models (LLMs).

The project separates application behavior from provider-specific integration code. Instead of importing and calling a model SDK directly inside the use case, the application communicates through an abstract contract named `LLMPort`.

The current implementation uses a concrete `GeminiAdapter` to communicate with Google Gemini. Because the application depends on the port rather than the adapter, another provider can be introduced without rewriting the core text-generation workflow.

The implemented flow:

- accepts a prompt through a Typer CLI,
- loads environment-based settings,
- constructs the configured provider adapter,
- injects the adapter into the application use case,
- sends the prompt through `LLMPort`,
- executes the provider-specific request,
- returns the generated text to the interface.

## Scope

| Capability | Current Behavior |
|---|---|
| Application use case | `GenerateText` executes the text-generation workflow |
| Provider contract | `LLMPort` defines the interface required by the application |
| Provider adapter | `GeminiAdapter` implements the current Gemini integration |
| Configuration | Settings are loaded from environment variables |
| Dependency injection | A concrete adapter is supplied to the use case |
| Execution model | Provider calls are asynchronous |
| Delivery | Typer-based command-line interface |
| Tests | Settings configuration and adapter initialization |
| Provider support | Google Gemini |
| Future direction | OpenAI, Groq, Anthropic, and other adapters |

The current project is intentionally narrow. It demonstrates provider decoupling and application structure rather than a complete production gateway platform.

Explicit non-goals in the current version include provider failover, request routing, streaming, retries, cost accounting, prompt governance, token-budget enforcement, persistent request history, and response-schema validation.

---

# 2. Problem Statement

Directly calling an LLM provider SDK from application code creates avoidable architectural coupling.

| Failure Mode | Engineering Impact |
|---|---|
| SDK calls inside business logic | Provider details spread into the application layer |
| Provider-specific request objects | Core use cases become difficult to reuse |
| Hard-coded API keys | Secrets become coupled to source code |
| Provider-specific exceptions | Error handling leaks across the codebase |
| Direct model selection in the CLI | Presentation logic becomes responsible for infrastructure |
| No abstraction boundary | Replacing a provider requires application changes |
| Synchronous blocking calls | Concurrency and responsiveness become harder to manage |
| Uncontrolled configuration | Environments behave inconsistently |
| Concrete dependencies in tests | Unit tests require SDKs, credentials, or network access |

A tightly coupled implementation often looks like this:

```text
CLI
 ↓
Gemini SDK
 ↓
Gemini API
```

In that structure, the CLI or use case must understand provider credentials, model configuration, SDK methods, request syntax, and response objects.

LLM Gateway introduces an explicit boundary:

```text
user prompt
    ↓
interface
    ↓
application use case
    ↓
LLMPort
    ↓
provider adapter
    ↓
provider API
```

The application owns the use case.

The adapter owns provider translation.

The provider SDK remains an infrastructure detail.

---

# 3. Architecture

```mermaid
flowchart TD
    USER["User"] --> CLI["Typer CLI"]
    CLI --> SETTINGS["Environment Settings"]
    CLI --> APP["GenerateText Use Case"]
    SETTINGS --> ADAPTER["GeminiAdapter"]
    APP --> PORT["LLMPort Protocol"]
    ADAPTER -. "implements" .-> PORT
    APP --> ADAPTER
    ADAPTER --> SDK["Gemini SDK"]
    SDK --> API["Gemini API"]
    API --> ADAPTER
    ADAPTER --> APP
    APP --> CLI
    CLI --> USER
```

The implementation follows a simplified Clean Architecture dependency rule:

> Application policy may depend on abstractions. Infrastructure details implement those abstractions.

## Dependency Direction

```text
Interfaces
    ↓
Application
    ↓
Ports

Infrastructure
    └── implements Ports
```

The important distinction is between **source-code dependency direction** and **runtime execution direction**.

At runtime, the application calls a concrete adapter. In source code, the application is designed against the `LLMPort` abstraction.

```mermaid
flowchart LR
    CLI["Interfaces"] --> USECASE["Application"]
    USECASE --> PORT["Port / Protocol"]
    ADAPTER["Infrastructure Adapter"] -. "implements" .-> PORT
    ADAPTER --> PROVIDER["External Provider"]
```

## Layer Responsibilities

| Layer | Responsibility | Excludes |
|---|---|---|
| Domain | Future provider-independent business concepts and rules | SDK calls, CLI parsing, environment loading |
| Application | Executes the text-generation use case | Gemini request construction and terminal formatting |
| Ports | Defines the provider capability required by the application | Concrete SDK implementation |
| Infrastructure | Implements provider communication and configuration | Application orchestration |
| Interfaces | Receives user input and presents output | Provider-specific request logic |

The application layer never needs to know whether the active implementation uses Gemini, OpenAI, Groq, Anthropic, a local model, or a test double.

---

# 4. Project Structure

```text
llm-gateway/
├── docs/
│   └── PROJECT_NOTE.md
├── evals/
├── tests/
├── src/
│   └── llm_gateway/
│       ├── application/
│       │   └── generate_text.py
│       ├── domain/
│       ├── infrastructure/
│       │   ├── gemini_adapter.py
│       │   └── settings.py
│       ├── interfaces/
│       │   └── cli.py
│       └── ports/
│           └── llm.py
├── README.md
└── pyproject.toml
```

## Directory Responsibilities

| Path | Responsibility |
|---|---|
| `docs/` | Engineering notes, architecture decisions, and production guidance |
| `evals/` | Future model-behavior and provider-comparison evaluations |
| `tests/` | Unit, integration, interface, and contract verification |
| `application/` | Use-case orchestration |
| `domain/` | Provider-independent domain concepts |
| `ports/` | Abstract contracts required by the application |
| `infrastructure/` | Provider adapters and environment configuration |
| `interfaces/` | CLI and future API, worker, or event interfaces |
| `pyproject.toml` | Package metadata, dependencies, scripts, and tooling |

Each directory represents a reason for change.

| Change | Expected Location |
|---|---|
| Text-generation workflow changes | `application/` |
| Provider contract changes | `ports/` |
| Gemini SDK changes | `infrastructure/gemini_adapter.py` |
| Environment settings change | `infrastructure/settings.py` |
| CLI commands or output change | `interfaces/cli.py` |
| Provider-independent model concepts | `domain/` |

Directory responsibilities should remain stable even if filenames evolve.

---

# 5. Provider Adapter Model

The central design separates three concepts:

```text
Use Case
   ↓ depends on
Port
   ↑ implemented by
Adapter
```

## Port

`LLMPort` describes the capability needed by the application.

Conceptually:

```python
from typing import Protocol


class LLMPort(Protocol):
    async def generate(self, prompt: str) -> str:
        ...
```

The port communicates application intent:

```text
Generate text from this prompt.
```

It should not expose unnecessary provider concepts such as SDK clients, provider response objects, transport sessions, or authentication classes.

## Adapter

`GeminiAdapter` translates the provider-independent operation into Gemini-specific behavior.

Conceptually:

```python
class GeminiAdapter:
    async def generate(self, prompt: str) -> str:
        # Translate the application request
        # Call Gemini
        # Translate the provider response
        # Return application-level text
        ...
```

## Provider SDK

The SDK is an external dependency used only inside infrastructure.

```text
Application language:
generate(prompt) -> text

Gemini language:
configure client
select model
construct request
await SDK operation
extract provider response text
```

The adapter performs this translation.

## Why a Protocol?

Python Protocols support structural typing.

A concrete class can satisfy `LLMPort` by implementing the required method shape, without inheriting from a shared base class.

This provides:

- low coupling,
- clear application contracts,
- simple test doubles,
- flexible adapter implementation,
- static type-checking support.

A Protocol defines what the application needs, not how a provider must be built.

---

# 6. Components

## 6.1 Application Use Case

The current application use case is:

```text
GenerateText
```

Its responsibility is to coordinate text generation through the port.

```mermaid
flowchart LR
    INPUT["Prompt"] --> USECASE["GenerateText"]
    USECASE --> PORT["LLMPort"]
    PORT --> RESULT["Generated Text"]
```

The use case should:

- accept application input,
- call the injected LLM abstraction,
- return provider-independent output,
- remain unaware of SDK initialization,
- remain unaware of environment variables,
- avoid CLI-specific formatting.

The use case should not:

- import the Gemini SDK,
- read `GEMINI_API_KEY`,
- choose terminal formatting,
- instantiate a provider internally,
- expose Gemini response objects,
- contain provider-specific retry logic.

A narrow use case is easier to test because a fake implementation of `LLMPort` can replace the real adapter.

---

## 6.2 LLM Port

The current port is:

```text
LLMPort
```

Responsibilities:

- define the text-generation capability,
- establish the method signature expected by the application,
- hide provider implementation details,
- support provider replacement,
- enable test doubles.

The port is an architectural boundary.

It is not a provider factory, configuration object, SDK wrapper collection, or universal representation of every possible provider feature.

A useful port should remain focused on application needs.

If future requirements introduce embeddings, structured output, image generation, audio, or streaming, those capabilities should be modeled deliberately rather than added indiscriminately to one oversized interface.

---

## 6.3 Gemini Adapter

The current concrete adapter is:

```text
GeminiAdapter
```

Responsibilities:

- initialize Gemini-specific dependencies,
- authenticate using configured credentials,
- translate the application prompt into the Gemini request format,
- execute the asynchronous provider call,
- extract generated text,
- translate provider failures into stable application-level errors when error handling is added.

```mermaid
flowchart LR
    PORTCALL["generate(prompt)"] --> TRANSLATE["Build Gemini Request"]
    TRANSLATE --> SDK["Gemini SDK"]
    SDK --> RESPONSE["Provider Response"]
    RESPONSE --> EXTRACT["Extract Text"]
    EXTRACT --> RETURN["Return str"]
```

The adapter is the only current component that should understand Gemini-specific SDK behavior.

When the Gemini SDK changes, most required modifications should remain inside this adapter.

---

## 6.4 Settings

Application settings are loaded from `.env` or the process environment.

Current configuration:

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Authenticates requests to Gemini |
| `LLM_PROVIDER` | Identifies the selected provider |
| `LLM_TIMEOUT_SECONDS` | Defines the intended request timeout policy |

Configuration separates deployment values from source code.

```text
source code
    +
environment configuration
    =
runtime behavior
```

Settings should provide:

- explicit field names,
- predictable defaults where appropriate,
- validation for required secrets,
- typed values,
- clear startup failures for invalid configuration.

Secrets must not be committed to source control.

Recommended files:

```text
.env              # local secret values; ignored by Git
.env.example      # documented variable names; no real secrets
```

---

## 6.5 Typer CLI

The current interface is a Typer command-line application.

Responsibilities:

- receive the prompt,
- load or receive application dependencies,
- invoke `GenerateText`,
- display the generated result,
- present user-facing failures.

```text
CLI input
    ↓
application input
    ↓
use-case execution
    ↓
application result
    ↓
CLI output
```

The CLI is a delivery mechanism, not the owner of provider logic.

A future FastAPI endpoint, background worker, scheduled job, or desktop interface should be able to reuse the same application use case.

---

## 6.6 Dependency Composition

The application requires a concrete object at runtime even though it depends on an abstraction in design.

Dependency composition connects the layers:

```python
settings = Settings()
adapter = GeminiAdapter(settings=settings)
use_case = GenerateText(llm=adapter)
result = await use_case.execute(prompt)
```

This wiring should occur at the application boundary or composition root.

```mermaid
flowchart TD
    CONFIG["Load Settings"] --> CREATE["Create GeminiAdapter"]
    CREATE --> INJECT["Inject into GenerateText"]
    INJECT --> EXECUTE["Execute Use Case"]
```

The composition root is allowed to know concrete classes.

The use case is not.

---

# 7. Request Execution Pipeline

```mermaid
flowchart TD
    A["Prompt Argument"] --> B["Typer CLI"]
    B --> C["Load Settings"]
    C --> D["Resolve Provider Adapter"]
    D --> E["Create GenerateText Use Case"]
    E --> F["Call LLMPort"]
    F --> G["Translate Provider Request"]
    G --> H["Gemini API"]
    H --> I["Receive Provider Response"]
    I --> J["Extract Text"]
    J --> K["Return Application Result"]
    K --> L["Display CLI Output"]
```

## Sequence

1. The user submits a prompt through the CLI.
2. The interface loads validated environment configuration.
3. The application creates or resolves the selected provider adapter.
4. The adapter is injected into `GenerateText`.
5. The use case calls the `LLMPort` operation.
6. `GeminiAdapter` translates the call into Gemini-specific SDK behavior.
7. The provider returns its response.
8. The adapter extracts provider-independent text.
9. The use case returns the text.
10. The CLI displays the result.

## Boundary Rule

```text
CLI input ≠ provider request object
provider response object ≠ application result
```

Translation occurs at boundaries.

This prevents the provider SDK from becoming the application’s internal data model.

---

# 8. Async Execution

The provider call is asynchronous because network operations spend most of their time waiting for external I/O.

Conceptually:

```python
result = await llm.generate(prompt)
```

Async execution supports:

- non-blocking provider calls,
- better concurrency in API or worker environments,
- future parallel requests,
- streaming integration,
- timeout and cancellation handling.

Async does not automatically provide:

- retries,
- concurrency limits,
- rate limiting,
- cancellation safety,
- provider failover,
- lower latency.

Those behaviors require explicit policy.

## Async Boundary

| Component | Expected Async Behavior |
|---|---|
| CLI | Runs the async application entry point |
| Application use case | Awaits the port |
| Port | Declares the async operation |
| Adapter | Awaits the provider SDK |
| Settings | Normally synchronous |
| Pure domain rules | Normally synchronous |

The async contract should follow the I/O path rather than spreading into components that perform only deterministic computation.

---

# 9. Configuration and Provider Resolution

The current project defines `LLM_PROVIDER`, but the initial implementation supports Gemini only.

A basic current resolution model is:

```text
LLM_PROVIDER=gemini
        ↓
create GeminiAdapter
```

A future provider factory may support:

```mermaid
flowchart TD
    SETTINGS["LLM_PROVIDER"] --> FACTORY["Provider Factory"]
    FACTORY --> CHECK{"Selected Provider"}
    CHECK -->|gemini| GEMINI["GeminiAdapter"]
    CHECK -->|openai| OPENAI["OpenAIAdapter"]
    CHECK -->|groq| GROQ["GroqAdapter"]
    CHECK -->|anthropic| ANTHROPIC["AnthropicAdapter"]
    CHECK -->|unknown| ERROR["Configuration Error"]
```

Provider resolution belongs in the composition layer.

It should not be placed inside `GenerateText`.

## Configuration Policy

| Condition | Recommended Behavior |
|---|---|
| Required API key missing | Fail during startup or dependency construction |
| Timeout is not numeric | Reject configuration |
| Timeout is zero or negative | Reject configuration |
| Unsupported provider | Return explicit configuration error |
| Provider-specific key missing | Reject only when that provider is selected |
| Secret appears in logs | Redact it |
| `.env` committed | Remove and rotate affected credentials |

A settings object should convert raw strings into validated application configuration before provider execution begins.

---

# 10. CLI Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Settings
    participant UseCase as GenerateText
    participant Port as LLMPort
    participant Adapter as GeminiAdapter
    participant Gemini as Gemini API

    User->>CLI: Submit prompt
    CLI->>Settings: Load configuration
    Settings-->>CLI: Valid settings
    CLI->>Adapter: Construct adapter
    CLI->>UseCase: Inject adapter
    CLI->>UseCase: Execute prompt
    UseCase->>Port: generate(prompt)
    Port->>Adapter: Runtime implementation
    Adapter->>Gemini: Async provider request
    Gemini-->>Adapter: Provider response
    Adapter-->>UseCase: Generated text
    UseCase-->>CLI: Application result
    CLI-->>User: Display text
```

Run the CLI:

```bash
python -m llm_gateway.interfaces.cli "Hello AI"
```

Example output:

```text
Hello! How can I help you today?
```

The exact response is provider-generated and may vary between executions.

The CLI proves end-to-end wiring, but a successful CLI response alone does not verify architecture, failure behavior, cost control, output quality, or production reliability.

---

# 11. Design Principles

## Clean Architecture

The project separates application policy from delivery and provider details.

```text
policy
  ↓
abstraction
  ↑
detail
```

The stable part of the system should not depend on the most volatile part.

Provider SDKs, API versions, authentication mechanisms, and response formats may change frequently. The application use case should remain comparatively stable.

## Dependency Inversion Principle

High-level application logic should not depend directly on a low-level provider module.

Both communicate through an abstraction:

```text
GenerateText → LLMPort ← GeminiAdapter
```

The arrow represents source-code dependency.

## Separation of Concerns

| Concern | Owner |
|---|---|
| Receive terminal input | CLI |
| Execute text-generation workflow | Application |
| Define required provider capability | Port |
| Call Gemini | Adapter |
| Load environment values | Settings |
| Select concrete dependencies | Composition root |

## Dependency Injection

The use case receives its dependency rather than constructing it internally.

```text
Preferred:
GenerateText(llm=adapter)

Avoid:
GenerateText creates GeminiAdapter itself
```

Injection improves substitution, testing, configuration, and lifecycle control.

## Interface-Driven Design

The application is designed around required behavior instead of a specific library.

The interface should be:

- small,
- explicit,
- provider-independent,
- aligned with application use cases,
- stable enough to support multiple implementations.

## Single Responsibility

Each component has one primary reason to change.

| Component | Changes When |
|---|---|
| `GenerateText` | Text-generation workflow changes |
| `LLMPort` | Required application capability changes |
| `GeminiAdapter` | Gemini integration changes |
| `Settings` | Configuration policy changes |
| CLI | Terminal interaction changes |
| Provider factory | Provider resolution rules change |

---

# 12. Design Decisions

| Decision | Rationale | Trade-off |
|---|---|---|
| Port between use case and provider | Prevents provider SDK coupling | Adds an abstraction |
| Python Protocol | Supports structural typing and simple test doubles | Runtime enforcement is limited |
| Adapter per provider | Isolates translation and SDK behavior | Requires one implementation per provider |
| Async provider method | Matches network I/O and future concurrency needs | Async execution must be managed |
| Environment-based settings | Separates deployment values and secrets from code | Configuration must be validated |
| Thin CLI | Keeps presentation separate from use-case policy | Dependency wiring must live elsewhere |
| Application-level string result | Prevents provider objects from leaking inward | Provider metadata is not yet exposed |
| Single current provider | Keeps learning scope focused | Multi-provider claims remain architectural, not implemented |
| Basic tests first | Verifies construction and configuration boundaries | Does not yet prove request behavior |
| Empty domain package | Preserves room for future domain concepts | Current project may appear structurally larger than its behavior |

## Port Granularity

A single `generate(prompt: str) -> str` operation is suitable for the present scope.

It may become insufficient when the product requires:

- system and user message separation,
- sampling parameters,
- tool calling,
- structured output,
- multimodal inputs,
- token usage,
- provider metadata,
- streaming events.

The port should evolve from real application requirements rather than mirror every feature offered by all providers.

---

# 13. Testing Strategy

The test suite should prove both deterministic architecture behavior and provider-boundary behavior.

## Current Coverage

The supplied project notes identify current tests for:

- settings configuration,
- Gemini adapter initialization.

Run:

```bash
pytest
```

Example project output:

```text
2 passed
```

The active repository run should remain the source of truth for current pass counts.

## Component Coverage

| Component | Required Cases |
|---|---|
| Settings | Valid values, missing API key, default provider, invalid timeout |
| `LLMPort` contract | Compatible fake and concrete implementations |
| `GenerateText` | Prompt forwarding, returned text, propagated application errors |
| Gemini adapter | Initialization, request translation, response extraction |
| Provider factory | Supported provider and unsupported provider |
| CLI | Valid prompt, configuration failure, provider failure, visible output |
| Async behavior | Awaited execution and cancellation/timeout behavior |

## Unit Test With a Fake Port

A use-case test should not require Gemini credentials or network access.

Conceptually:

```python
class FakeLLM:
    async def generate(self, prompt: str) -> str:
        return f"fake:{prompt}"


async def test_generate_text_uses_port():
    use_case = GenerateText(llm=FakeLLM())

    result = await use_case.execute("Hello")

    assert result == "fake:Hello"
```

This test proves application behavior independently of the provider SDK.

## Adapter Test Boundary

Adapter tests should verify translation behavior without making uncontrolled live requests.

Useful techniques include:

- mocking the SDK client,
- injecting a provider client,
- using recorded fixtures where permitted,
- separating unit tests from live smoke tests.

## Test Pyramid

```text
many fast unit tests
        ↓
fewer adapter integration tests
        ↓
minimal live provider smoke tests
```

Live tests should be explicitly marked because they consume credentials, network access, time, and potentially money.

## Boundary Matrix

| Case | Expected Result |
|---|---|
| Valid configuration | Dependency construction succeeds |
| Missing Gemini key | Explicit configuration failure |
| Valid prompt | Use case forwards prompt once |
| Adapter returns text | Use case returns the same application-level text |
| Provider returns empty result | Apply documented empty-response policy |
| Provider raises an error | Translate or propagate according to error policy |
| Unsupported provider | Reject before use-case execution |
| Timeout reached | Cancel or fail with a stable timeout error |
| Fake port supplied | Unit test runs without network access |
| CLI receives invalid input | Return readable interface error |

---

# 14. Error Boundary

Provider failures should not leak uncontrolled SDK exception types across the entire application.

A future stable error model may include:

```text
LLMConfigurationError
LLMAuthenticationError
LLMRateLimitError
LLMTimeoutError
LLMProviderUnavailableError
LLMInvalidResponseError
LLMRequestError
```

```mermaid
flowchart LR
    SDKERROR["Provider SDK Error"] --> ADAPTER["Adapter Translation"]
    ADAPTER --> APPERROR["Application-Level Error"]
    APPERROR --> INTERFACE["CLI Presentation"]
```

## Error Ownership

| Failure | Owner |
|---|---|
| Missing environment variable | Settings |
| Unsupported provider | Factory or composition root |
| Invalid application input | Interface or application validation |
| Gemini authentication failure | Gemini adapter |
| Provider timeout | Adapter and timeout policy |
| User-facing error message | CLI |
| Retry decision | Application/infrastructure resilience policy |

The CLI should display useful information without exposing API keys, internal stack traces, or provider response payloads containing sensitive data.

---

# 15. Security and Data Handling

An LLM gateway crosses a trust boundary between product input and an external provider.

| Risk | Required Control |
|---|---|
| API-key exposure | Store secrets in environment or a secret manager |
| Secret logging | Redact credentials and authorization headers |
| Prompt data leakage | Define provider data-handling and retention policy |
| Sensitive user input | Classify, minimize, and redact where required |
| Prompt injection | Separate trusted instructions from untrusted content |
| Unbounded requests | Integrate token and request-budget validation |
| Provider misuse | Apply authentication, authorization, and quotas at service boundaries |
| Cross-tenant leakage | Isolate request context, logs, and metadata |
| Unsafe output | Validate or moderate at the response boundary |
| Dependency compromise | Pin, scan, and update SDK dependencies |

Recommended request metadata:

```text
request_id
provider
model
timeout
input_size
status
latency
error_code
token_usage
estimated_cost
```

Raw prompts and responses should not be logged by default when they may contain private or business-sensitive information.

## Secret Management

```text
Local development:
.env file ignored by Git

CI/CD:
encrypted repository or platform secrets

Production:
managed secret store with rotation and access control
```

A real API key must never appear in:

- source code,
- README examples,
- committed `.env` files,
- test fixtures,
- exception messages,
- screenshots,
- public logs.

---

# 16. Production Considerations

## Provider Factory

A provider factory should map validated configuration to a concrete adapter.

```python
def build_llm(settings: Settings) -> LLMPort:
    if settings.llm_provider == "gemini":
        return GeminiAdapter(...)
    raise UnsupportedProviderError(settings.llm_provider)
```

The factory is a construction mechanism.

It should not contain prompt policy or application workflow logic.

## Timeouts

`LLM_TIMEOUT_SECONDS` should become an enforced runtime policy rather than a documented setting only.

Timeout behavior should define:

- connection timeout,
- total request timeout,
- cancellation behavior,
- retry eligibility,
- user-facing error mapping.

## Retries

Retries should be limited to failures that may succeed on a later attempt.

| Failure | Typical Retry Decision |
|---|---|
| Temporary network interruption | Retry with backoff |
| Provider 5xx response | Retry within policy |
| Rate limit | Retry only with provider guidance and budget |
| Authentication failure | Do not retry |
| Invalid request | Do not retry |
| Content-policy rejection | Do not retry unchanged |
| Timeout | Retry only when idempotency and budget allow |

Retry policy should include:

- maximum attempts,
- exponential backoff,
- jitter,
- total deadline,
- retryable error classification,
- request idempotency,
- cost impact.

## Provider Failover

Provider failover is not merely an additional `try/except`.

Different providers may vary in:

- model capability,
- token limits,
- message format,
- safety behavior,
- tool-calling support,
- structured-output support,
- pricing,
- latency,
- response quality.

Failover requires an explicit compatibility and product policy.

## Streaming

Streaming changes the port contract from one returned string to a sequence of events or chunks.

```text
request
   ↓
stream start
   ↓
content chunks
   ↓
usage metadata
   ↓
completion or failure
```

A streaming port may be separate from the simple text-generation port to avoid forcing all implementations into one interface.

## Observability

Production telemetry should measure:

- request count by provider and model,
- success and failure rates,
- latency percentiles,
- timeout frequency,
- retry count,
- rate-limit frequency,
- token usage,
- estimated and actual cost,
- empty-response frequency,
- adapter error categories,
- provider fallback frequency.

Metrics should use stable application error codes rather than arbitrary SDK exception strings.

## Lifecycle Management

Provider clients may hold HTTP sessions, connection pools, or other resources.

A production composition root should define:

- client creation,
- client reuse,
- startup validation,
- graceful shutdown,
- connection cleanup,
- concurrency limits.

---

# 17. Integration With Related Projects

The gateway can become the provider-execution boundary for other AI product engineering components.

## Prompt Contract Integration

```mermaid
flowchart LR
    CONTRACT["Prompt Contract"] --> VALIDATE["Validate and Render"]
    VALIDATE --> PROMPT["Rendered Prompt"]
    PROMPT --> GATEWAY["LLM Gateway"]
    GATEWAY --> PROVIDER["Provider Adapter"]
```

The Prompt Contract component should prepare deterministic provider input.

The gateway should execute it.

## Request Budget Guard Integration

```mermaid
flowchart LR
    REQUEST["LLM Request"] --> BUDGET["Request Budget Guard"]
    BUDGET --> DECISION{"Accepted?"}
    DECISION -->|No| REJECT["Budget Error"]
    DECISION -->|Yes| GATEWAY["LLM Gateway"]
    GATEWAY --> PROVIDER["Provider"]
```

The Budget Guard should reject oversized or over-budget requests before the gateway spends tokens or money.

## Combined Product Pipeline

```mermaid
flowchart TD
    INPUT["User Input"] --> CONTRACT["Prompt Contract"]
    CONTRACT --> BUDGET["Request Budget Guard"]
    BUDGET --> GATEWAY["LLM Gateway"]
    GATEWAY --> ADAPTER["Provider Adapter"]
    ADAPTER --> MODEL["LLM Provider"]
    MODEL --> OUTPUT["Raw Model Output"]
    OUTPUT --> VALIDATOR["Response Validation"]
    VALIDATOR --> PRODUCT["Product Response"]
```

Each component owns a distinct boundary:

| Component | Responsibility |
|---|---|
| Prompt Contract | Define and validate prompt construction |
| Request Budget Guard | Enforce context and cost policy |
| LLM Gateway | Abstract and execute provider communication |
| Response Validator | Verify output shape and policy |
| Product Interface | Deliver the final result |

---

# 18. Evaluation Boundary

Unit and integration tests answer:

```text
Did the application call the configured provider boundary correctly?
```

Model evaluations answer:

```text
Did the selected provider and model produce an acceptable response?
```

These are different questions.

## Engineering Tests

- Was the prompt forwarded correctly?
- Was the adapter selected correctly?
- Was the response translated correctly?
- Were provider errors mapped correctly?
- Was configuration validated?
- Did the call respect the timeout?

## Model Evaluations

- Was the answer accurate?
- Did the model follow instructions?
- Was the response format correct?
- Did quality change between providers?
- Did a model upgrade create regressions?
- Is latency and cost acceptable for the quality level?

Future evaluation records should include:

```text
test_case_id
gateway_version
provider
model
model_parameters
prompt_digest
response
grader_result
latency
input_tokens
output_tokens
cost
error_code
```

The gateway enables provider substitution, but evaluations determine whether a substitution is acceptable for the product.

---

# 19. Current Limitations

- Only Google Gemini is implemented.
- Provider factory behavior is not yet established as a complete multi-provider system.
- Test coverage is currently limited.
- Retry behavior is not implemented.
- Enforced timeout handling is not demonstrated.
- Streaming responses are not implemented.
- Structured output is not modeled.
- Provider error translation is not defined.
- Logging and metrics are not implemented.
- Token usage is not recorded.
- Cost tracking is not implemented.
- Rate limiting is not implemented.
- Provider failover is not implemented.
- Prompt Contract integration is not implemented.
- Request Budget Guard integration is not implemented.
- Response validation is not implemented.
- Persistent request history is not implemented.
- Authentication and authorization are not implemented for a service interface.
- The current interface is CLI-only.
- The domain layer does not yet contain substantial domain behavior.

These constraints define the current project boundary. They should not be presented as implemented production capabilities.

---

# 20. Future Improvements

| Priority | Improvement | Engineering Outcome |
|---:|---|---|
| 1 | Use-case tests with a fake port | Verify application logic without network access |
| 2 | Provider factory | Resolve adapters from validated configuration |
| 3 | Stable error model | Prevent SDK exception leakage |
| 4 | Enforced timeout policy | Bound request latency |
| 5 | Retry with backoff and jitter | Recover from transient failures safely |
| 6 | OpenAI adapter | Demonstrate provider substitution |
| 7 | Groq adapter | Add another provider execution path |
| 8 | Anthropic adapter | Expand provider compatibility |
| 9 | Structured request model | Support model parameters without SDK leakage |
| 10 | Streaming port | Deliver incremental model output |
| 11 | Logging and metrics | Observe latency, failures, and provider behavior |
| 12 | Token and cost tracking | Measure request consumption |
| 13 | Prompt Contract integration | Add validated prompt preparation |
| 14 | Request Budget Guard integration | Reject unsafe or expensive requests early |
| 15 | Response validation | Enforce typed or schema-based outputs |
| 16 | FastAPI interface | Expose the use case as a service |
| 17 | Docker support | Standardize execution environments |
| 18 | CI/CD | Automate tests, linting, typing, and release checks |

Additional candidates include provider health checks, circuit breakers, concurrency control, caching, model routing, provider failover, usage quotas, tracing, secret-manager integration, and evaluation-driven provider selection.

---

# 21. Key Takeaways

- Application use cases should depend on provider capabilities, not provider SDKs.
- `LLMPort` defines what the application needs.
- `GeminiAdapter` translates that need into Gemini-specific behavior.
- The adapter owns provider request and response translation.
- The application layer should not read provider credentials or instantiate SDK clients.
- Python Protocols support flexible, structurally typed boundaries.
- Dependency injection makes provider replacement and unit testing easier.
- Async execution is appropriate for provider network I/O.
- Environment configuration separates deployment values from source code.
- A thin CLI prevents provider policy from spreading into the interface.
- Multi-provider architecture does not mean multi-provider behavior is already implemented.
- Retries, timeouts, streaming, cost tracking, and failover require explicit product policies.
- Prompt preparation, budget validation, provider execution, and response validation are separate engineering boundaries.
- Provider substitution must be verified by both engineering tests and model evaluations.

---

# 22. Learning Outcomes

Through this project, I learned:

- how the Provider Adapter Pattern works,
- why provider SDKs should remain infrastructure details,
- how Clean Architecture controls dependency direction,
- how the Dependency Inversion Principle protects high-level policy,
- how Python Protocols define structural interfaces,
- how dependency injection enables substitution,
- how to separate use cases from interfaces,
- how to load configuration from environment variables,
- how async provider calls fit into an application workflow,
- how to organize a Python project using a professional `src/` layout,
- how to prepare an application for additional providers,
- how unit tests can replace external providers with fakes,
- why production reliability requires more than a working SDK call.

---

# 23. Project Completion Gate

```text
IMPLEMENTATION
[ ] LLMPort contract defined
[ ] GenerateText use case implemented
[ ] GeminiAdapter implemented
[ ] Environment settings implemented
[ ] Typer CLI implemented
[ ] Async provider call working

VERIFICATION
[ ] Settings tests passing
[ ] Adapter initialization test passing
[ ] Use case tested with a fake port
[ ] Prompt forwarding verified
[ ] Provider response extraction verified
[ ] Configuration failures verified
[ ] CLI success path verified
[ ] CLI failure path verified

ARCHITECTURE
[ ] Application does not import Gemini SDK
[ ] Provider details remain inside infrastructure
[ ] Dependency injection occurs at the composition boundary
[ ] Interface remains thin
[ ] Secrets remain outside source control

PRODUCTION UNDERSTANDING
[ ] Timeout policy understood
[ ] Retry policy understood
[ ] Provider error translation understood
[ ] Streaming contract impact understood
[ ] Cost and token tracking boundary understood
[ ] Prompt Contract integration boundary understood
[ ] Request Budget Guard integration boundary understood
```

The checklist should be updated from the active repository state rather than marked complete only because the architecture is documented.

---

# 24. Final Recall Map

```mermaid
flowchart TD
    A["LLM REQUEST"] --> B["RECEIVE"]
    B --> C["CONFIGURE"]
    C --> D["RESOLVE"]
    D --> E["ADAPT"]
    E --> F["EXECUTE"]
    F --> G["RETURN"]

    B -.-> B1["Accept input through an interface"]
    C -.-> C1["Load validated environment settings"]
    D -.-> D1["Select and construct the provider adapter"]
    E -.-> E1["Translate through LLMPort"]
    F -.-> F1["Await the provider call"]
    G -.-> G1["Return provider-independent text"]
```

## Memory Hook

```text
RECEIVE
→ accept the prompt

CONFIGURE
→ load valid settings

RESOLVE
→ construct the selected provider

ADAPT
→ translate application intent

EXECUTE
→ call the external model

RETURN
→ expose an application-level result
```

---

# 25. Interview Recall

You should be able to answer these without notes:

1. What problem does the Provider Adapter Pattern solve?
2. Why should `GenerateText` depend on `LLMPort` instead of `GeminiAdapter`?
3. What is the difference between a port and an adapter?
4. Why is the provider SDK an infrastructure detail?
5. How do Python Protocols support dependency inversion?
6. Why is dependency injection better than constructing the adapter inside the use case?
7. Where should provider selection occur?
8. Why should the CLI remain thin?
9. What should the Gemini adapter translate?
10. Why should provider response objects not leak into the application layer?
11. Why are async methods useful for LLM calls?
12. What does async execution not solve automatically?
13. How can `GenerateText` be tested without a Gemini API key?
14. What errors should be translated at the adapter boundary?
15. What is the difference between an engineering test and a model evaluation?
16. Why does adding another adapter not automatically guarantee equivalent behavior?
17. Where should retry and timeout policies live?
18. How would streaming change the port contract?
19. How should Prompt Contract Lab integrate with the gateway?
20. How should Request Budget Guard integrate with the gateway?

---

# 26. Project Status

```text
IMPLEMENTED
→ LLMPort abstraction
→ GenerateText application use case
→ Gemini provider adapter
→ Environment-based configuration
→ Typer CLI
→ Async provider request path

CURRENTLY VERIFIED
→ Settings configuration
→ Gemini adapter initialization
→ Basic CLI execution path described by the project

NOT YET IMPLEMENTED
→ Multiple provider adapters
→ Provider factory
→ Stable provider error model
→ Retry mechanism
→ Enforced timeout handling
→ Streaming
→ Logging and observability
→ Token and cost tracking
→ Prompt Contract integration
→ Request Budget Guard integration
→ Response-schema validation
→ FastAPI service boundary
```

---

# Conclusion

LLM Gateway demonstrates how an AI application can communicate with an external model provider without allowing provider-specific code to control the application architecture.

The central boundary is `LLMPort`.

`GenerateText` depends on that abstraction, while `GeminiAdapter` implements it using Gemini-specific SDK behavior. This arrangement applies the Provider Adapter Pattern, Dependency Inversion Principle, dependency injection, and separation of concerns in a practical LLM application.

The current system remains intentionally lightweight. It does not yet provide the operational features expected from a production gateway, such as multiple providers, retries, enforced timeouts, streaming, observability, cost tracking, or response validation.

Its value is architectural: the project establishes a clean provider boundary that future capabilities can build upon without rewriting the application use case.

---

# License

MIT License.
