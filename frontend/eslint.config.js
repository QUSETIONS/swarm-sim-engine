import globals from "globals";
import tsParser from "@typescript-eslint/parser";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import vuePlugin from "eslint-plugin-vue";
import vueParser from "vue-eslint-parser";

export default [
    {
        ignores: ["dist/", "node_modules/", "*.config.*"],
    },
    // TypeScript files
    {
        files: ["**/*.ts"],
        languageOptions: {
            parser: tsParser,
            ecmaVersion: "latest",
            sourceType: "module",
            globals: globals.browser,
        },
        plugins: {
            "@typescript-eslint": tsPlugin,
        },
        rules: {
            "no-unused-vars": "off",
            "@typescript-eslint/no-unused-vars": ["warn", { argsIgnorePattern: "^_" }],
            "@typescript-eslint/no-explicit-any": "off",
        },
    },
    // Vue SFC files
    {
        files: ["**/*.vue"],
        languageOptions: {
            parser: vueParser,
            parserOptions: {
                parser: tsParser,
                ecmaVersion: "latest",
                sourceType: "module",
            },
            globals: globals.browser,
        },
        plugins: {
            vue: vuePlugin,
        },
        rules: {
            ...vuePlugin.configs["vue3-recommended"].rules,
            "vue/multi-word-component-names": "off",
            "vue/singleline-html-element-content-newline": "off",
            "vue/html-self-closing": "off",
        },
    },
];
