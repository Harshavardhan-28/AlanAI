FROM node:20-alpine

RUN corepack enable && corepack prepare pnpm@9.15.0 --activate

WORKDIR /repo

COPY pnpm-workspace.yaml package.json ./
COPY packages/shared/typescript ./packages/shared/typescript
COPY apps/web ./apps/web

RUN pnpm install --frozen-lockfile=false

EXPOSE 3000
CMD ["pnpm", "--filter", "web", "dev"]
