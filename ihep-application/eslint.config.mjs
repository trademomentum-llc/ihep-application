import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    // Emscripten-generated USD/WASM bindings (vendored build output, not source).
    "public/wasm/**",
    // Vendored, minified Chart.js bundle (third-party build output).
    "src/app/investor-dashboard/chart.js",
  ]),
  // Node CommonJS build/maintenance scripts legitimately use require().
  {
    files: ["scripts/**/*.js", "**/*.cjs"],
    rules: { "@typescript-eslint/no-require-imports": "off" },
  },
]);

export default eslintConfig;
