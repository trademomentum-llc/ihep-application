declare module '@/server/storage' {
  export const storage: Record<string, (...args: unknown[]) => Promise<unknown>>
}

