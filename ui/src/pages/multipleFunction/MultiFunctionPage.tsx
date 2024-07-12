import React, { useState } from 'react';
import { Upload, Button, Checkbox, message, Spin } from 'antd';
import ReactPlayer from 'react-player';
import { UploadOutlined } from '@ant-design/icons';
import './MultiFunctionPage.css';

const { Group: CheckboxGroup } = Checkbox;

const MultiFunctionPage: React.FC = () => {
    const [mode, setMode] = useState<string[]>([]);
    const [sourceVideo, setSourceVideo] = useState<string | null>(null);
    const [targetVideo, setTargetVideo] = useState<string | null>(null);
    const [resultVideo, setResultVideo] = useState<string | null>(null);
    const [detectionVideo, setDetectionVideo] = useState<string | null>(null);
    const [selectedModels, setSelectedModels] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [detectionResults, setDetectionResults] = useState<string[]>([]);

    const handleUpload = (file: any, type: string) => {
        const url = URL.createObjectURL(file);
        if (type === 'source') setSourceVideo(url);
        if (type === 'target') setTargetVideo(url);
        if (type === 'detection') setDetectionVideo(url);
        return false; // Prevent automatic upload
    };

    const handleStartGeneration = () => {
        setLoading(true);
        setTimeout(() => {
            setLoading(false);
            const generatedVideoUrl = "path/to/generated/video"; // 这里应该是生成的视频URL
            setResultVideo(generatedVideoUrl);
            if (mode.includes('detection')) {
                handleStartDetection(generatedVideoUrl);
            }
        }, 2000);
    };

    const handleStartDetection = (videoUrl: string | null = null) => {
        setLoading(true);
        setTimeout(() => {
            setLoading(false);
            const results = selectedModels.map(model => `Detection complete using model: ${model}`);
            setDetectionResults(results);
            results.forEach(result => {
                message.success(result);
            });
        }, 2000);
    };

    const handleModeChange = (checkedValues: string[]) => {
        setMode(checkedValues);
        // 重置所有状态
        setSourceVideo(null);
        setTargetVideo(null);
        setResultVideo(null);
        setDetectionVideo(null);
        setSelectedModels([]);
        setDetectionResults([]);
    };

    const isGenerationDisabled = !sourceVideo || !targetVideo;
    const isDetectionDisabled = !detectionVideo || selectedModels.length === 0;

    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <div className="checkbox-container">
                <CheckboxGroup
                    options={['generation', 'detection']}
                    onChange={handleModeChange}
                    value={mode}
                    style={{ marginBottom: '20px' }}
                />
            </div>
            {mode.includes('generation') && (
                <div className="video-container">
                    <div className="video-group">
                        <div className="video-upload">
                            <Upload beforeUpload={file => handleUpload(file, 'source')} showUploadList={false}>
                                <Button icon={<UploadOutlined />}>Upload Source Video</Button>
                            </Upload>
                            {sourceVideo && <ReactPlayer url={sourceVideo} controls />}
                        </div>
                        <div className="video-upload">
                            <Upload beforeUpload={file => handleUpload(file, 'target')} showUploadList={false}>
                                <Button icon={<UploadOutlined />}>Upload Target Video</Button>
                            </Upload>
                            {targetVideo && <ReactPlayer url={targetVideo} controls />}
                        </div>
                    </div>
                    {mode.includes('detection') && (
                        <div className="checkbox-container">
                            <CheckboxGroup
                                options={['model1', 'model2', 'model3']}
                                onChange={checkedValues => setSelectedModels(checkedValues as string[])}
                                value={selectedModels}
                                style={{ margin: '20px 0' }}
                            />
                        </div>
                    )}
                    <div className="button-container">
                        <Button
                            type="primary"
                            onClick={handleStartGeneration}
                            disabled={isGenerationDisabled}
                        >
                            Start Generation
                        </Button>
                    </div>
                </div>
            )}
            {resultVideo && (
                <div className="result-video">
                    <ReactPlayer url={resultVideo} controls />
                </div>
            )}
            {mode.includes('detection') && (
                <div className="detection-container">
                    {!mode.includes('generation') && (
                        <>
                            <Upload beforeUpload={file => handleUpload(file, 'detection')} showUploadList={false}>
                                <Button icon={<UploadOutlined />}>Upload Detection Video</Button>
                            </Upload>
                            <div className="checkbox-container">
                                <CheckboxGroup
                                    options={['model1', 'model2', 'model3']}
                                    onChange={checkedValues => setSelectedModels(checkedValues as string[])}
                                    value={selectedModels}
                                    style={{ margin: '20px 0' }}
                                />
                            </div>
                        </>
                    )}
                    {(!mode.includes('generation') && detectionVideo) && <ReactPlayer url={detectionVideo} controls />}
                    {!mode.includes('generation') && (
                        <Button
                            type="primary"
                            onClick={() => handleStartDetection(detectionVideo)}
                            disabled={isDetectionDisabled}
                        >
                            Start Detection
                        </Button>
                    )}
                </div>
            )}
            {loading && <Spin style={{ marginTop: '20px' }} />}
            {detectionResults.length > 0 && (
                <div className="detection-results">
                    <h3>Detection Results</h3>
                    <ul>
                        {detectionResults.map((result, index) => (
                            <li key={index}>{result}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default MultiFunctionPage;
