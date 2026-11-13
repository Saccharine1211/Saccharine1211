<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg"/>
  <img src="assets/header-dark.svg" width="100%" alt="Jimin Kim — Backend Engineer, owning Infra"/>
</picture>

<a href="mailto:rlawlals031211@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
<a href="https://github.com/Softbank-Hackathon-2026-Team-Echo"><img src="https://img.shields.io/badge/Team_Echo-EchoPort-F59E0B?style=for-the-badge&logo=github&logoColor=white" alt="Team Echo"/></a>

</div>

## 🎯 Now & Next

**Now** — I run the servers and the production environment of a B2B service at MORI Corp. Alongside feature work, more of my time goes to the things that keep the service up: deployments and releases, monitoring and alerts, and access control.

**Next** — As the company grows, so do traffic and the amount of work to process. I am preparing in two directions.

**1. Distributing large-scale traffic**
- **Load balancing and autoscaling**: keep response times when traffic spikes
- **Asynchronous processing**: move heavy work onto queues to keep the request path light
- **Scaling the data layer**: connection pooling, read replicas, caching
- **Scaling by measurement**: find the limits first with load tests and SLOs, then decide when to scale

**2. Hybrid on-premises + cloud**
- **Steady load on-premises, bursts in the cloud**: run the baseline cheaply on our own servers and send only the spikes to the cloud
- **Heavy compute on-premises**: run GPU-type work, which is expensive in the cloud, on in-house servers
- **One way to operate every environment**: deploy and observe on-premises with the same containers, GitOps and telemetry as the cloud
- **Connections that survive outages**: connect through tunnels or VPNs with no inbound ports, and let the cloud take over on failure

I have already tried part of this at hackathons. In EchoPort, an on-premises k3s cluster was connected through Cloudflare Tunnel: pulling the cable moved traffic to the cloud, and plugging it back in returned it with no human action (about 19 s to switch). In Likelion, users registered their own on-premises servers over Tailscale and received deployments through the same GitOps flow as the cloud clusters. I am now taking this experience, together with staged traffic shifting between clouds and connection pooling, to the scale of a real service.

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 🧭 What I bring

| Area | What I have done |
|---|---|
| **Backend** | Design and build service APIs and platform control-plane APIs, with audit logs, idempotency and failure records from day one (Node.js · FastAPI) |
| **Infra · IaC** | Move hand-made resources into Terraform and CDK, deploy with OIDC instead of long-lived keys, reconcile with Argo CD |
| **Deployment platforms** | Owned the server and infra side of two deployment platforms at hackathons: zero-downtime multi-cloud migration (EchoPort) and one-click GitOps deployment (Likelion) |
| **Operations** | Run the release train and CI runners at work, with SLO-breach alerts and runbooks. I report measurements, failed-request counts and rollback paths rather than "it works" |
| **Observability** | Attached OpenTelemetry collectors and Prometheus remote write to three environments (AWS · GCP · on-premises) the same way |
| **Security** | Least-privilege IAM per job, an image vulnerability gate (Trivy), CVE watching from the OSV feed |

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 📌 Featured

<p align="center">
<a href="https://github.com/Softbank-Hackathon-2026-Team-Echo"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/echoport-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/echoport-light.svg"/>
  <img src="assets/cards/echoport-dark.svg" width="49%" alt="EchoPort — SoftBank Hackathon 2026 Finals, 2nd place"/>
</picture></a>
<a href="#mori"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/contentcare-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/contentcare-light.svg"/>
  <img src="assets/cards/contentcare-dark.svg" width="49%" alt="MORI ContentCare"/>
</picture></a>
</p>
<p align="center">
<a href="https://github.com/2026-softbank-1"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/likelion-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/likelion-light.svg"/>
  <img src="assets/cards/likelion-dark.svg" width="49%" alt="Likelion — Team Iris"/>
</picture></a>
<a href="https://github.com/Saccharine1211/event-driven-media-processing-demo"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/media-pipeline-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/media-pipeline-light.svg"/>
  <img src="assets/cards/media-pipeline-dark.svg" width="49%" alt="Event-Driven Media Processing Demo"/>
</picture></a>
</p>

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 🩺 Troubleshooting log

> Production-style incidents I traced and fixed myself. Each link opens the PR with the root-cause analysis and the rollout record.

| Problem | Cause | Fix | Result |
|---|---|---|---|
| AWS PgBouncer → GCP DB connection **timed out** during the DB migration | Packets from pods on a secondary ENI were SNATed to the primary ENI address and dropped by the VPC (kube-proxy DNAT applied before the CNI connmark) | Enabled external SNAT in EKS vpc-cni, restarted the two nodes one at a time | Path restored; **0 of 149** client requests failed during the change · [PR](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/141) |
| **About 23 s with no writes** in a cutover rehearsal | After PgBouncer RESUME, it waited for the default `server_login_retry` of 15 s (measured 14.7 s) | Retry interval 15 → 1 s, applied first on the side opposite the current writer | Finals rehearsal: writes paused **about 10 s, 0 failed writes** · [PR](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/143) |
| The security gate **blocked deployments to all three environments** | A new HIGH vulnerability in `apt` in the base image (unrelated to app code) | Removed the package managers (apt · pip) from the runtime image | HIGH finding gone, and new `apt` CVEs can no longer block deploys · [PR](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-demo-app/pull/5) |

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 💼 Experience

<a id="mori"></a>

### MORI Corp. — Lead Engineer <sub>Sep 2025 – present · Incheon, South Korea</sub>

> I build and run **ContentCare**, a B2B content protection service. Reporting directly to the CEO, I lead server development and also own cloud infrastructure, releases and operations. Top committer in 7 of the company's 8 main repositories; **1,186 merged PRs** across 14 company repositories. <sub>(Company repositories are private, so internals are not described here.)</sub>
>
> `Node.js` `Python` `AWS` `IaC` `GitHub Actions` `Self-hosted runner` `Docker`

- Design, build and operate the service API servers
- Codify the production cloud infrastructure; least privilege per job and masking of sensitive data in logs
- Run the release train and deployment automation, including self-hosted CI runners
- SLO evaluation, breach alerts and incident runbooks
- Cost control by starting and stopping GPU jobs automatically
- Mobile app builds and store releases

### 🏆 SoftBank Hackathon 2026, Finals — 2nd place (Excellence Award), Team Echo <sub>Oct 30 – Nov 8, 2026</sub>

> **EchoPort**: a multi-cloud BCDR platform that moves running services between AWS, GCP and on-premises without stopping them when a disaster hits, and moves them back the same way afterwards. I owned the control-plane API server and the infrastructure and migration engine for the three environments it manages. The demo environments were torn down after the event; the code is in the [Team Echo organization](https://github.com/Softbank-Hackathon-2026-Team-Echo).
>
> Demo result: emergency migration **AWS Tokyo → GCP Seoul in 11 s, 0 of 149 probe requests failed**
>
> `FastAPI` `PostgreSQL` `Terraform` `EKS` `GKE` `k3s` `Envoy` `PgBouncer` `cert-manager` `OpenTelemetry` `Cloudflare Tunnel`

<details>
<summary><b>Show main work</b></summary>

**Multi-cloud infrastructure ([echo-infra](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra))**
- Moved hand-made runner secrets, Cloudflare and cert-manager setup **into Terraform**; codified the AWS Load Balancer Controller IAM
- Split a GKE cluster for customer workloads away from the control plane and moved the Seoul DB onto it
- Ingress: **DNS-01 wildcard** certificates for the shared GKE ingress via cert-manager, per-service Envoy weights and host isolation, a Cloudflare load-balancer switch path
- OpenTelemetry collectors in all three environments plus Prometheus remote write from the ingress
- On-premises k3s that comes up the same way on any Linux machine, connected through a tunnel with no inbound ports
- CI authenticates with OIDC instead of cloud keys; runner identity, permissions and label policy kept separate

**Migration engine · data cutover**
- Six-step traffic migration (5 → 10 → 25 → 50 → 75 → 100%), each step judged by **N requests actually served**, with automatic rollback on failure
- Switched the DB writer with PostgreSQL logical replication plus PgBouncer PAUSE/RESUME, recording cutover and rollback results in the DB
- Traced cutover failures: fixed a cross-cloud DB path timeout with EKS vpc-cni external SNAT; reconnect wait 15 → 1 s

**Control-plane API ([echo-was](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was))**
- Real build, deploy and teardown executors, plus EKS · GKE · k3s connectivity adapters; automatic production deploy on push to main
- Live earthquake feed (USGS) → **automatic emergency migration plans** for services in affected environments
- Failed deploy → AI diagnosis in an isolated sandbox → human approval → redeploy from the fix commit

**Security · supply chain**
- Environment × control security matrix with time-boxed exceptions and audit logs; CVE watching from the OSV feed
- Removed apt · pip from runtime images to clear HIGH findings; published amd64 · arm64 images to GHCR

</details>

### SoftBank Hackathon 2026, Preliminaries — Team Iris <sub>Oct 2026</sub>

> **[Likelion](https://github.com/2026-softbank-1)**: a GitOps deployment platform that takes pushed code all the way through build, deploy, failure diagnosis and a fix PR. I owned the platform API server, the multi-cluster deploy targets and the on-premises connection. 133 merged PRs.
>
> `FastAPI` `Argo CD` `ApplicationSet` `Helm` `EKS` `GKE` `Tailscale`

<details>
<summary><b>Show main work</b></summary>

- Added **GCP (GKE)** and **users' own on-premises servers** as deploy targets: ApplicationSet, gateway and IAM, automated registration and connection over Tailscale, heartbeat-based disconnect status
- Removed sync delay by having Argo CD receive GitOps pushes by webhook; zero-downtime replacement with a pre-stop wait in service pods
- **Console Gateway** that relays on-premises runtime logs and pod shells through Argo CD
- `likelion` CLI operations commands and LLM agent support, releases v0.3 – v0.4.3

</details>

## 🎓 Education

**Tech University of Korea** — Entered 2023, currently on leave of absence

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 🛠️ Stack

**Backend**

<p align="center">
  <img src="https://skillicons.dev/icons?i=py,fastapi,nodejs,ts,postgres,redis,dynamodb&perline=7&theme=dark" alt="Backend"/>
</p>

**Infra · Ops**

<p align="center">
  <img src="https://skillicons.dev/icons?i=aws,gcp,kubernetes,terraform,docker,cloudflare,githubactions,prometheus,linux&perline=9&theme=dark" alt="Infra"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Argo_CD-EF7B4D?style=flat-square&logo=argo&logoColor=white"/>
  <img src="https://img.shields.io/badge/k3s-FFC61C?style=flat-square&logo=k3s&logoColor=black"/>
  <img src="https://img.shields.io/badge/Envoy-AC6199?style=flat-square&logo=envoyproxy&logoColor=white"/>
  <img src="https://img.shields.io/badge/PgBouncer-336791?style=flat-square&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenTelemetry-425CC7?style=flat-square&logo=opentelemetry&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS_CDK-FF9900?style=flat-square&logo=amazonwebservices&logoColor=white"/>
  <img src="https://img.shields.io/badge/Helm-0F1689?style=flat-square&logo=helm&logoColor=white"/>
  <img src="https://img.shields.io/badge/Trivy-1904DA?style=flat-square&logo=aqua&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tailscale-242424?style=flat-square&logo=tailscale&logoColor=white"/>
</p>


## 🔄 Recently

<!-- The three columns below are rewritten daily by GitHub Actions (scripts/update_readme.py). Public repositories only. -->
<table><tr><td valign="top" width="34%">

#### Recently merged PRs
<!-- recent_prs starts -->
- [docs: 데모 서비스 종료 안내 + 영어 요약](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/154)<br><sub>echo-infra · 2026-11-13</sub>
- [docs: 데모 서비스 종료 안내 + 영어 요약](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was/pull/148)<br><sub>echo-was · 2026-11-13</sub>
- [docs: 데모 서비스 종료 안내 + 영어 요약](https://github.com/Softbank-Hackathon-2026-Team-Echo/.github/pull/1)<br><sub>.github · 2026-11-13</sub>
- [fix: EKS vpc-cni 외부 SNAT 켜기 — A PgBouncer→B DB ClusterIP …](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/141)<br><sub>echo-infra · 2026-11-08</sub>
- [perf: 이전 비율 단계 확인 간격 단축(설정)](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was/pull/145)<br><sub>echo-was · 2026-11-07</sub>
<!-- recent_prs ends -->

</td><td valign="top" width="33%">

#### Recently reviewed PRs
<!-- recent_reviews starts -->
- [feat: 이전 승인·실행 시작 보안 게이트 (보안·거버넌스 5, 기본 꺼짐)](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was/pull/61)<br><sub>echo-was · 2026-11-06</sub>
- [feat: 빌드 비밀 검사에서 C-SEC-1 비밀 전달 경로 증거를 만든다 (보안·거버넌스 2-4)](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was/pull/74)<br><sub>echo-was · 2026-11-06</sub>
- [feat: AWS를 GCP에서 구독할 수 있게 열고, 명령어로 적용한 인프라 패치를 코드로 명시화한다.](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/45)<br><sub>echo-infra · 2026-11-05</sub>
<!-- recent_reviews ends -->

</td><td valign="top" width="33%">

#### Recently active repositories
<!-- recent_repos starts -->
- [echo-infra](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra)<br><sub>EchoPort 인프라와 이전 엔진. Terraform · EKS · GKE · …</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-13</sub>
- [echo-was](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was)<br><sub>EchoPort 관리 평면 API. 환경 · 배포 · 이전 계획 · 재난 · 보안…</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-13</sub>
- [echo-demo-app](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-demo-app)<br><sub>시연용 관리 대상 앱. 순번 쓰기로 이전 중 누락 · 중복 확인</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-08</sub>
- [echo-ai-agent](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-ai-agent)<br><sub>EchoPort AI 에이전트 러너. 격리 샌드박스에서 점검 · 수정 · 검증</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-08</sub>
- [hoshi-words](https://github.com/Shin-Bi/hoshi-words)<br><sub>별빛 단어 공개 데모 — 직접 작성한 단어·예문과 Flutter 학습 화면, An…</sub><br><sub>Shin-Bi · 2026-11-05</sub>
<!-- recent_repos ends -->

</td></tr></table>

## 📊 Activity

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/stats-light.svg"/>
  <img src="assets/stats-dark.svg" width="100%" alt="GitHub contribution stats"/>
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Saccharine1211/Saccharine1211/output/snake-dark.svg"/>
  <img src="https://raw.githubusercontent.com/Saccharine1211/Saccharine1211/output/snake.svg" width="100%" alt="Contribution snake"/>
</picture>

<sub>Stats are redrawn daily by GitHub Actions</sub>

</div>
