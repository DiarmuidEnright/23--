import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
    reactStrictMode: true,
    webpack(config) {
      config.module.rules.push({
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: 'asset/resource',
      });
      return config;
    },
  };


export default nextConfig;
