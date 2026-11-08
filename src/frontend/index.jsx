import React, { useEffect, useState } from 'react';
import ForgeReconciler, {
    Text,
    Heading,
    Badge,
    Button,
    ButtonGroup,
    SectionMessage,
    Stack,
    Inline,
    Box,
    ProgressBar,
    TagGroup,
    Tag,
    Lozenge,
    Spinner
} from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);
    const [remediating, setRemediating] = useState(false);
    const [generatingDoc, setGeneratingDoc] = useState(false);
    const [remediationReceipt, setRemediationReceipt] = useState(null);
    const [postMortemResult, setPostMortemResult] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);

    const loadContext = async () => {
        try {
            setLoading(true);
            setErrorMessage(null);
            const res = await invoke('getIssueContext');
            setData(res);
        } catch (err) {
            setErrorMessage(err.message || 'Failed to fetch issue context');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadContext();
    }, []);

    const handleRemediate = async (actionId) => {
        try {
            setRemediating(true);
            const res = await invoke('executeRemediation', {
                actionId,
                driftScore: data?.analysis?.driftScore,
                rootCause: data?.analysis?.rootCause
            });
            setRemediationReceipt(res);
        } catch (err) {
            setErrorMessage(err.message || 'Failed to execute remediation');
        } finally {
            setRemediating(false);
        }
    };

    const handleGeneratePostMortem = async () => {
        try {
            setGeneratingDoc(true);
            const res = await invoke('generatePostMortem', {
                spaceKey: 'ENG'
            });
            setPostMortemResult(res?.postMortemPage);
        } catch (err) {
            setErrorMessage(err.message || 'Failed to publish Confluence retrospective');
        } finally {
            setGeneratingDoc(false);
        }
    };

    if (loading) {
        return (
            <Stack space="space.200" alignInline="center">
                <Spinner size="large" />
                <Text>SentinelForge is traversing Teamwork Graph and analyzing drift...</Text>
            </Stack>
        );
    }

    if (errorMessage) {
        return (
            <SectionMessage appearance="error" title="SentinelForge Analysis Error">
                <Text>{errorMessage}</Text>
                <Button appearance="subtle" onClick={loadContext}>Retry</Button>
            </SectionMessage>
        );
    }

    const analysis = data?.analysis || {};
    const graph = data?.graph || {};
    const driftScore = analysis.driftScore || 0;
    const riskLevel = analysis.riskLevel || 'LOW';
    const blastRadius = analysis.blastRadius || [];

    let badgeAppearance = 'success';
    if (riskLevel === 'CRITICAL' || riskLevel === 'HIGH') {
        badgeAppearance = 'removed';
    } else if (riskLevel === 'MODERATE') {
        badgeAppearance = 'inprogress';
    }

    return (
        <Stack space="space.200">
            <Inline space="space.100" alignBlock="center" spread="space-between">
                <Heading size="medium">SentinelForge Sentinel</Heading>
                <Lozenge appearance="success">Teamwork Graph & MCP Active</Lozenge>
            </Inline>

            {remediationReceipt && (
                <SectionMessage appearance="confirmation" title="Automated Remediation Dispatched">
                    <Text>
                        Action applied: {remediationReceipt.actionId}. Receipt logged in Jira comments at {new Date(remediationReceipt.remediatedAt).toLocaleTimeString()}.
                    </Text>
                </SectionMessage>
            )}

            {postMortemResult && (
                <SectionMessage appearance="information" title="Confluence Retrospective Published">
                    <Text>
                        Published to {postMortemResult.spaceKey} space: "{postMortemResult.title}". Cross-linked to Jira ticket activity.
                    </Text>
                </SectionMessage>
            )}

            <Box backgroundColor="color.background.accent.gray.subtlest" padding="space.150">
                <Stack space="space.100">
                    <Inline space="space.100" alignBlock="center" spread="space-between">
                        <Text weight="bold">System Configuration Drift</Text>
                        <Lozenge appearance={badgeAppearance}>{riskLevel} RISK ({driftScore}%)</Lozenge>
                    </Inline>
                    <ProgressBar value={driftScore / 100} />
                    <Text size="small">
                        Root Cause: {analysis.rootCause || 'No variance detected across graph nodes.'}
                    </Text>
                </Stack>
            </Box>

            <Stack space="space.100">
                <Text weight="bold">Connected Teamwork Graph Nodes ({graph.connectedNodes?.length || 0})</Text>
                <TagGroup>
                    {graph.connectedNodes?.map((node, idx) => (
                        <Tag 
                            key={idx} 
                            text={`${node.type}: ${node.title || node.name || node.sha}`} 
                            color={node.type === 'CONFLUENCE_PAGE' ? 'blue' : node.type === 'GIT_COMMIT' ? 'purple' : 'green'} 
                        />
                    ))}
                </TagGroup>
            </Stack>

            {blastRadius.length > 0 && (
                <Stack space="space.100">
                    <Text weight="bold">Infrastructure Blast Radius Matrix</Text>
                    {blastRadius.map((item, idx) => (
                        <Box key={idx} padding="space.100" backgroundColor="color.background.elevation.surface.sunken">
                            <Inline space="space.100" alignBlock="center" spread="space-between">
                                <Text weight="medium">{item.service} ({item.tier})</Text>
                                <Lozenge appearance={item.status === 'DEGRADED' ? 'removed' : item.status === 'MONITORING' ? 'inprogress' : 'success'}>
                                    {item.status}
                                </Lozenge>
                            </Inline>
                            <Text size="small">{item.impact} • Owner: {item.owner}</Text>
                        </Box>
                    ))}
                </Stack>
            )}

            {analysis.anomalies?.length > 0 && (
                <Stack space="space.100">
                    <Text weight="bold">Detected Anomalies</Text>
                    {analysis.anomalies.map((anomaly, idx) => (
                        <Inline key={idx} space="space.100" alignBlock="center">
                            <Badge appearance={anomaly.severity === 'HIGH' ? 'primary' : 'default'}>
                                {anomaly.severity}
                            </Badge>
                            <Text size="small">{anomaly.message}</Text>
                        </Inline>
                    ))}
                </Stack>
            )}

            <Stack space="space.150">
                <Text weight="bold">Remediation & Retrospective Controls</Text>
                <ButtonGroup>
                    <Button 
                        appearance="primary" 
                        isLoading={remediating} 
                        onClick={() => handleRemediate('ACTION_APPLY_THROTTLE')}
                    >
                        Apply Queue Circuit Breaker
                    </Button>
                    <Button 
                        appearance="default" 
                        isLoading={generatingDoc}
                        onClick={handleGeneratePostMortem}
                    >
                        Generate Confluence Post-Mortem
                    </Button>
                    <Button appearance="subtle" onClick={loadContext}>
                        Refresh Audit
                    </Button>
                </ButtonGroup>
            </Stack>
        </Stack>
    );
};

ForgeReconciler.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
