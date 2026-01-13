import {defineConfig, globalIgnores} from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import globals from "globals";
import path from "node:path";
import {
	fileURLToPath
} from "node:url";
import js from "@eslint/js";
import {
	FlatCompat
} from "@eslint/eslintrc";
import stylistic from "@stylistic/eslint-plugin";
import tseslint from "typescript-eslint";
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
	baseDirectory: __dirname,
	recommendedConfig: js.configs.recommended,
	allConfig: js.configs.all
});

export default defineConfig([
	...nextVitals,
	...nextTs,
	...compat.extends("eslint:recommended"),
	...tseslint.configs.recommended,
	globalIgnores([
		// Default ignores of eslint-config-next:
		".next/**",
		"out/**",
		"build/**",
		"next-env.d.ts",
		"node_modules/**",
		"components/ui/**"
	]),

	{
		files: ["**/*.{ts,js,tsx,jsx,cjs,mjs,cts,mts}"],
		languageOptions: {
			globals: {
				...globals.browser
			},
			ecmaVersion: 13,
			sourceType: "module"
		},
		rules: {
			"no-unused-vars": ["warn", {
				"caughtErrors": "none",
				"vars": "local",
				"args": "after-used",
				"ignoreRestSiblings": true
			}],
			"no-undef": "off",
			"no-useless-escape": "warn",
			"no-redeclare": "error",


			// Error Prevention & Best Practices
			"no-eval": "error",
			"no-implied-eval": "error",
			"no-new-func": "error",
			"no-debugger": "error",
			"no-empty": "error",
			"no-unreachable": "error",
			"no-fallthrough": "error",
			"no-duplicate-case": "error",

			// Equality and Comparison
			"eqeqeq": ["error", "always"],
			"no-eq-null": "error",

			// ES6+ Best Practices
			"no-param-reassign": "error",
			// "object-shorthand": "warn",
			"no-duplicate-imports": "error",

			// Function Quality

			"consistent-return": "warn",



			// Performance and Memory
			"no-loop-func": "warn",
			"no-new-wrappers": "error",
			"no-array-constructor": "error",
			"no-new-object": "error",

			// Class-specific Rules
			"class-methods-use-this": "off",
			"no-useless-constructor": "error",
			"no-dupe-class-members": "error",
			"@typescript-eslint/no-this-alias": ["error", {"allowedNames": ["self"]}],

			// ES6+ Best Practices
			"prefer-const": "error",
			"no-var": "error",
			"prefer-arrow-callback": "warn",
			"prefer-template": "warn",


			// Function Quality
			"max-params": ["warn", 10]
		}
	},
	stylistic.configs["disable-legacy"],
	{
		files: ["**/*.{ts,js,tsx,jsx,cjs,mjs,cts,mts}"],
		plugins: {
			"@stylistic": stylistic
		},
		rules: {
			// indentation
			"@stylistic/indent": ["error", "tab", {
				"SwitchCase": 1,
				"ignoredNodes": [
					"VariableDeclaration[declarations.length > 1] > VariableDeclarator"
				]
			}],
			"@stylistic/no-multi-spaces": ["error", {"ignoreEOLComments": true}],
			"@stylistic/indent-binary-ops": ["error", "tab"],
			"@stylistic/no-mixed-spaces-and-tabs": ["error", "smart-tabs"],
			"@stylistic/no-trailing-spaces": ["error"],
			"@stylistic/no-whitespace-before-property": ["error"],




			// stylistic (formatting) rules
			"@stylistic/array-bracket-newline": ["error", "consistent"],
			"@stylistic/array-bracket-spacing": ["error", "never"],

			"@stylistic/arrow-parens": ["error", "always"],
			"@stylistic/arrow-spacing": ["error", {"before": true, "after": true}],

			"@stylistic/block-spacing": ["error", "always"],
			"@stylistic/brace-style": ["error", "1tbs", {"allowSingleLine": true}],

			"@stylistic/comma-dangle": ["error", "never"],
			"@stylistic/comma-spacing": ["error", {"before": false, "after": true}],
			"@stylistic/comma-style": ["error", "last"],

			"@stylistic/computed-property-spacing": ["error", "never"],
			"@stylistic/dot-location": ["error", "property"],

			"@stylistic/eol-last": ["error", "always"],
			"@stylistic/function-call-spacing": ["error", "never"],

			"@stylistic/function-paren-newline": ["error", "multiline"],
			"@stylistic/generator-star-spacing": ["error", {"before": false, "after": true}],
			"@stylistic/yield-star-spacing": ["error", {"before": false, "after": true}],

			"@stylistic/implicit-arrow-linebreak": ["error", "beside"],

			"@stylistic/key-spacing": ["error"],

			"@stylistic/keyword-spacing": ["error", {"before": true, "after": true}],

			"@stylistic/linebreak-style": "off",
			"@stylistic/lines-between-class-members": ["error", "always", {"exceptAfterSingleLine": true}],


			"@stylistic/multiline-ternary": ["error", "always-multiline"],
			"@stylistic/new-parens": ["error", "always"],
			"@stylistic/no-confusing-arrow": ["error", {"allowParens": true, "onlyOneSimpleParam": true}],
			"@stylistic/no-extra-parens": ["error", "functions"],
			"@stylistic/no-extra-semi": ["error"],
			"@stylistic/no-floating-decimal": ["error"],
			"@stylistic/no-mixed-operators": ["error"],

			"@stylistic/nonblock-statement-body-position": ["error", "beside"],
			"@stylistic/quote-props": ["error", "consistent"],
			"@stylistic/quotes": ["warn", "double", {"allowTemplateLiterals": "always"}],
			"@stylistic/rest-spread-spacing": ["error", "never"],
			"@stylistic/semi": ["error", "always"],
			"@stylistic/semi-spacing": ["error", {"before": false, "after": false}],
			"@stylistic/semi-style": ["error", "last"],
			"@stylistic/space-before-blocks": ["error", "never"],
			"@stylistic/space-before-function-paren": ["error", {
				"anonymous": "always",
				"named": "never",
				"asyncArrow": "always",
				"catch": "always"
			}],
			"@stylistic/space-in-parens": ["error", "never"],
			"@stylistic/space-infix-ops": ["error", {"int32Hint": false}],
			"@stylistic/space-unary-ops": ["error"],
			"@stylistic/switch-colon-spacing": ["error"],
			"@stylistic/template-tag-spacing": ["error", "never"],
			"@stylistic/wrap-iife": ["error", "inside"],
			"@stylistic/wrap-regex": ["error"],

			// curly bracket rules
			"@stylistic/object-curly-newline": ["error"],
			"@stylistic/object-curly-spacing": ["error", "never"],
			"@stylistic/template-curly-spacing": ["error", "never"],


			// operator
			"@stylistic/operator-linebreak": ["error", "before"],

			// ts
			"@stylistic/member-delimiter-style": ["error"],
			"@stylistic/type-annotation-spacing": ["error", {
				"before": false,
				"after": true,
				"overrides": {
					"arrow": {
						"before": true,
						"after": true
					}
				}
			}],
			"@stylistic/type-generic-spacing": ["error"],
			"@stylistic/type-named-tuple-spacing": ["error"]

		}
	}
]);
