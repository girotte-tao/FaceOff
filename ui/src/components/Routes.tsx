import React, { lazy } from 'react';
import { RouteObject } from 'react-router-dom';
import HomePage from '../pages/main/main';
import VideoPlayerPage from '../pages/detection/DetectionPage';
import MultiFunctionPage from "../pages/multipleFunction/MultiFunctionPage";

interface RouteConfig {
    path: string;
    Component: React.FC;
    label: string;
    key: string;
}

const routes: RouteConfig[] = [
    // {
    //     path: '/',
    //     Component: HomePage,
    //     label: 'Home',
    //     key: 'home',
    // },
    // {
    //     path: '/video-player',
    //     Component: VideoPlayerPage,
    //     label: 'Video Player',
    //     key: 'video-player',
    // },
    {
        path: '/Pipeline',
        Component: MultiFunctionPage,
        label: 'Pipeline',
        key: 'multi-function',
    },
];

export default routes;
