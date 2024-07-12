import React, { useState } from 'react';
import { Upload, Button, Select, message } from 'antd';
import ReactPlayer from 'react-player';
import { UploadOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Option } = Select;

const DetectionPage: React.FC = () => {
    const [videoUrl, setVideoUrl] = useState<string | null>(null);
    const [model, setModel] = useState<string>('');

    const handleUpload = (file: any) => {
        const url = URL.createObjectURL(file);
        setVideoUrl(url);
        return false; // Prevent automatic upload
    };

    const handleDetect = () => {
        if (!videoUrl) {
            message.error('Please upload a video first.');
            return;
        }
        if (!model) {
            message.error('Please select a model.');
            return;
        }
        // axios.post('/api/detect', { videoUrl, model })
        //     .then(response => {
        //         message.success('Detection successful');
        //         // Handle the response data as needed
        //     })
        //     .catch(error => {
        //         message.error('Detection failed');
        //     });
    };

    return (
        <div style={{ padding: '20px' }}>
            <Upload beforeUpload={handleUpload} showUploadList={false}>
                <Button icon={<UploadOutlined />}>Upload Video</Button>
            </Upload>
            {videoUrl && <ReactPlayer url={videoUrl} controls />}
            <Select
                placeholder="Select a model"
                style={{ width: 200, margin: '20px 0' }}
                onChange={value => setModel(value)}
            >
                <Option value="model1">Model 1</Option>
                <Option value="model2">Model 2</Option>
                <Option value="model3">Model 3</Option>
            </Select>
            <Button type="primary" onClick={handleDetect}>Detect</Button>
        </div>
    );
};

export default DetectionPage;
