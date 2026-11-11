<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg"/>
  <img src="assets/header-dark.svg" width="100%" alt="Jimin Kim — Backend & Infra Engineer"/>
</picture>

<a href="mailto:rlawlals031211@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
<a href="https://github.com/Softbank-Hackathon-2026-Team-Echo"><img src="https://img.shields.io/badge/Team_Echo-EchoPort-F59E0B?style=for-the-badge&logo=github&logoColor=white" alt="Team Echo"/></a>
<a href="https://app.echoport.uk"><img src="https://img.shields.io/badge/Live-app.echoport.uk-0EA5E9?style=for-the-badge&logo=cloudflare&logoColor=white" alt="EchoPort live"/></a>

</div>

## ⚙️ How I work

| 영역 | 이렇게 일합니다 |
|---|---|
| **API 서버** | 계약(OpenAPI)부터 정하고, 감사 로그 · 멱등성 · 실패 기록을 처음부터 넣습니다 |
| **인프라** | 손으로 만든 리소스는 Terraform/CDK로 옮기고, 키 대신 OIDC로 배포합니다 |
| **운영** | 「됐다」 대신 숫자로 말합니다 — 리허설 실측, 실패 요청 수, 롤백 경로 |

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 📌 Featured

<p align="center">
<a href="https://github.com/Softbank-Hackathon-2026-Team-Echo"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cards/echoport-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/cards/echoport-light.svg"/>
  <img src="assets/cards/echoport-dark.svg" width="49%" alt="EchoPort — SoftBank Hackathon 2026 본선 우수상(2위)"/>
</picture></a>
<a href="#mori--contentcare"><picture>
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

> 운영 중에 직접 원인을 찾고 고친 장애입니다. 링크를 누르면 원인 분석과 적용 기록이 남은 PR로 갑니다.

| 문제 | 원인 | 해결 | 결과 |
|---|---|---|---|
| DB 이전 중 AWS PgBouncer → GCP DB 연결 **시간 초과** | 보조 ENI 파드의 패킷이 주 ENI 주소로 SNAT되어 VPC가 버림 (kube-proxy DNAT가 CNI connmark보다 먼저 적용) | EKS vpc-cni 외부 SNAT 켜기, 노드 2대 순차 재시작 | 경로 복구, 적용 중 손님 요청 **149건 실패 0** · [PR](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/141) |
| 컷오버 리허설에서 **쓰기 공백 약 23초** | PgBouncer RESUME 뒤 `server_login_retry` 기본값 15초를 기다림 (14.7초) | 재시도 간격 15 → 1초, 쓰기 담당 반대쪽부터 순차 적용 | 본선 리허설 쓰기 정지 **10초 전후 · 쓰기 실패 0** · [PR](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/143) |
| 보안 게이트가 **세 환경 배포를 모두 차단** | 베이스 이미지의 `apt`에서 HIGH 취약점 새로 발견 (앱 코드와 무관) | 실행 이미지에서 패키지 관리자(apt · pip) 제거 | HIGH 취약점 제거, apt에 새 취약점이 나와도 다시 막히지 않는 구조 · [PR](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-demo-app/pull/5) |

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 💼 Experience

### 🏆 SoftBank Hackathon 2026 본선 우수상(2위) — Team Echo <sub>2026.10.30 ~ 11.08</sub>

> 재난이 오면 돌아가는 서비스를 AWS · GCP · 온프레미스 사이에서 **멈추지 않고 옮기고**, 끝나면 같은 절차로 되돌리는 멀티 클라우드 BCDR 플랫폼 **[EchoPort](https://app.echoport.uk)**. 관리 평면 API 서버와 인프라, 시연 앱을 맡았습니다.
>
> `FastAPI` `SQLAlchemy(async)` `PostgreSQL 논리 복제` `PgBouncer` `Envoy` `EKS` `GKE` `k3s` `Terraform` `cert-manager` `OpenTelemetry` `Cloudflare`

<details>
<summary><b>주요 작업 펼쳐보기</b></summary>

**API 서버 ([echo-was](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was))**
- 실제 빌드 · 배포 · 내리기 실행기와 운영 일꾼 — EKS · GKE · 온프렘 k3s 접속 확인 어댑터
- 트래픽 이전 6단계(5 → 10 → 25 → 50 → 75 → 100%) — 단계마다 **요청 N건 처리 확인**으로 판정, 실패 시 자동 롤백
- DB 쓰기 전환(컷오버) Job 생성 · 대기 · 판정을 이전 계획에 넣고 결과를 계획 상세에 연결
- 실제 지진 피드(USGS)로 재난 이벤트 → 피해 환경 서비스의 **긴급 이전 계획 자동 생성**
- 배포 실패 → AI 진단 → 사람 승인 → 서비스 저장소 커밋 · PR → **같은 커밋으로 재배포**
- 보안 매트릭스 · 기한부 예외 · 감사 로그 API, OSV 피드 기반 CVE 감시
- 운영 결과: 긴급 이전 **AWS 도쿄 → GCP 서울 11초, 판정 요청 149건 중 실패 0건**

**인프라 ([echo-infra](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra))**
- 손으로 만든 실행기 비밀 · Cloudflare · cert-manager를 **Terraform으로 이전**, AWS LB Controller IAM 코드화
- GKE 공유 진입점 인증서를 cert-manager **DNS-01 와일드카드**로, 서비스별 Envoy 가중치 · host 격리
- 세 환경 OTel 수집기 + 진입점 Prometheus remote write
- 온프레미스 k3s를 아무 리눅스 기기에 같은 방법으로 세우고, 인바운드 포트 없이 터널로 연결
- 컷오버 장애 추적 — EKS vpc-cni 외부 SNAT로 PgBouncer → DB 경로 타임아웃 해결, 재접속 대기 15 → 1초

**시연 앱 ([echo-demo-app](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-demo-app))**
- 순번 쓰기로 이전 중 **누락 · 중복**을 바로 보는 앱, Prometheus `/metrics`, amd64 · arm64 이미지 GHCR 게시
- 실행 이미지에서 apt · pip를 지워 HIGH 취약점 제거

</details>

### 주식회사 모리 — 리드 엔지니어 <sub>2025.09 ~ 재직 중</sub>

> B2B 콘텐츠 보안 서비스 **ContentCare**를 만들고 운영합니다. 대표 바로 아래에서 서버 · 클라우드 인프라 · 앱 출시까지 개발 전반을 맡고 있고, 사내 주요 레포 8곳 중 7곳에서 커밋 수 1위입니다. 사내 레포 14곳에서 **PR 1,186개 병합**. <sub>(사내 레포는 비공개)</sub>
>
> `Node.js` `Python` `AWS` `Docker` `GitHub Actions` `Flutter`

- 서비스 API 서버 설계 · 개발 · 운영
- 클라우드 인프라 구성과 코드화, 배포 자동화
- 모바일 앱 빌드 · 스토어 출시 · 운영 대응

### SoftBank Hackathon 2026 예선 — Team Iris <sub>2026.10</sub>

> 코드만 올리면 빌드 · 배포 · 장애 진단 · 수정 PR까지 해 주는 배포 자동화 플랫폼 **[Likelion](https://github.com/2026-softbank-1)**. PR 133개 병합.
>
> `FastAPI` `Argo CD` `EKS` `GKE` `Helm` `Tailscale` `TypeScript CLI`

<details>
<summary><b>주요 작업 펼쳐보기</b></summary>

- 배포 타깃에 **GCP(GKE)** 와 **사용자 온프레미스 서버** 추가 — 등록 · 연결 자동화, 하트비트로 연결 끊김 표시, 삭제 시 Tailscale 기기 정리
- 온프렘 런타임 로그 · Pod 셸을 Argo CD 경유로 중계하는 **Console Gateway** + ticket API
- Argo CD가 GitOps push를 webhook으로 바로 받게 해 동기화 지연 제거
- `likelion` CLI 운영 명령 · LLM 에이전트 지원, v0.3 ~ v0.4.3 릴리스

</details>

<div align="center"><picture><source media="(prefers-color-scheme: light)" srcset="assets/divider-light.svg"/><img src="assets/divider-dark.svg" width="100%" alt=""/></picture></div>

## 🛠️ Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=nodejs,express,ts,py,fastapi,postgres,redis,dynamodb&perline=8&theme=dark" alt="Backend"/>
  <br/>
  <img src="https://skillicons.dev/icons?i=aws,gcp,kubernetes,terraform,docker,cloudflare,githubactions,prometheus,linux&perline=9&theme=dark" alt="Infra"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Argo_CD-EF7B4D?style=flat-square&logo=argo&logoColor=white"/>
  <img src="https://img.shields.io/badge/Envoy-AC6199?style=flat-square&logo=envoyproxy&logoColor=white"/>
  <img src="https://img.shields.io/badge/AWS_CDK-FF9900?style=flat-square&logo=amazonwebservices&logoColor=white"/>
  <img src="https://img.shields.io/badge/k3s-FFC61C?style=flat-square&logo=k3s&logoColor=black"/>
  <img src="https://img.shields.io/badge/OpenTelemetry-425CC7?style=flat-square&logo=opentelemetry&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tailscale-242424?style=flat-square&logo=tailscale&logoColor=white"/>
  <img src="https://img.shields.io/badge/Sentry-362D59?style=flat-square&logo=sentry&logoColor=white"/>
</p>

## 🔄 Recently

<!-- 아래 세 칸은 GitHub Actions(scripts/update_readme.py)가 매일 다시 씁니다. 공개 저장소 활동만 나옵니다. -->
<table><tr><td valign="top" width="34%">

#### 최근 병합한 PR
<!-- recent_prs starts -->
- [feat: DB 정합성 표시 — 「DB 맞추는 중」 · 토폴로지 「DB 쓰기 담당」 · 「DB 일치 ·…](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-frontend/pull/129)<br><sub>echo-frontend · 2026-11-08</sub>
- [feat: demo-onprem 「환경 상태」 카드를 빼고 온프레 장애 · 전환 · 복구를 토폴로지 안…](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-frontend/pull/128)<br><sub>echo-frontend · 2026-11-08</sub>
- [fix: EKS vpc-cni 외부 SNAT 켜기 — A PgBouncer→B DB ClusterIP …](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/141)<br><sub>echo-infra · 2026-11-08</sub>
- [chore: 진입점 보조 VM b 제거 — 진입점 VM 하나만 (#112)](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/144)<br><sub>echo-infra · 2026-11-08</sub>
- [perf: 이전 비율 단계 확인 간격 단축(설정)](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was/pull/145)<br><sub>echo-was · 2026-11-07</sub>
<!-- recent_prs ends -->

</td><td valign="top" width="33%">

#### 최근 리뷰한 PR
<!-- recent_reviews starts -->
- [feat: 이전 승인·실행 시작 보안 게이트 (보안·거버넌스 5, 기본 꺼짐)](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was/pull/61)<br><sub>echo-was · 2026-11-06</sub>
- [feat: 빌드 비밀 검사에서 C-SEC-1 비밀 전달 경로 증거를 만든다 (보안·거버넌스 2-4)](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was/pull/74)<br><sub>echo-was · 2026-11-06</sub>
- [feat: AWS를 GCP에서 구독할 수 있게 열고, 명령어로 적용한 인프라 패치를 코드로 명시화한다.](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra/pull/45)<br><sub>echo-infra · 2026-11-05</sub>
- [docs: 시연 대본 초안과 보안 계약을 최신 서버 모양으로 정리](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-frontend/pull/62)<br><sub>echo-frontend · 2026-11-05</sub>
<!-- recent_reviews ends -->

</td><td valign="top" width="33%">

#### 최근 작업한 저장소
<!-- recent_repos starts -->
- [echo-infra](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-infra)<br><sub>EchoPort 인프라와 이전 엔진. Terraform · EKS · GKE · …</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-08</sub>
- [echo-demo-app](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-demo-app)<br><sub>시연용 관리 대상 앱. 순번 쓰기로 이전 중 누락 · 중복 확인</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-08</sub>
- [echo-frontend](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-frontend)<br><sub>EchoPort 웹 콘솔. 대시보드 · 서비스 · 대피 · 이전 · 보안 화면</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-08</sub>
- [echo-ai-agent](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-ai-agent)<br><sub>EchoPort AI 에이전트 러너. 격리 샌드박스에서 점검 · 수정 · 검증</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-08</sub>
- [echo-was](https://github.com/Softbank-Hackathon-2026-Team-Echo/echo-was)<br><sub>EchoPort 관리 평면 API. 환경 · 배포 · 이전 계획 · 재난 · 보안…</sub><br><sub>Softbank-Hackathon-2026-Team-Echo · 2026-11-08</sub>
<!-- recent_repos ends -->

</td></tr></table>

## 📊 Activity

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="assets/stats-light.svg"/>
  <img src="assets/stats-dark.svg" width="100%" alt="GitHub 기여 통계"/>
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Saccharine1211/Saccharine1211/output/snake-dark.svg"/>
  <img src="https://raw.githubusercontent.com/Saccharine1211/Saccharine1211/output/snake.svg" width="100%" alt="Contribution snake"/>
</picture>

<sub>통계는 매일 GitHub Actions가 다시 그립니다</sub>

</div>
