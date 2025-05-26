console.log('Jest configuration loaded');
// jest.config.mjs
export default {
  preset: 'ts-jest',
  testEnvironment: '@happy-dom/jest-environment',
  setupFilesAfterEnv: ['<rootDir>/src/tests/setupTests.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testMatch: ['<rootDir>/src/tests/**/*.(test|spec).tsx'],
};