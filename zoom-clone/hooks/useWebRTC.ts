import { useEffect, useRef, useState } from "react";

type SignalMessage = {
  type: string;
  from?: number;
  to?: number;
  data?: any;
  participant_id?: number;
  participants?: number[];
  display_name?: string;
};

type RemoteStream = {
  participantId: number;
  stream: MediaStream;
};

export function useWebRTC(
  meetingCode: string,
  token: string,
) {
  const socketRef = useRef<WebSocket | null>(null);
  const localStreamRef = useRef<MediaStream | null>(null);
  const peersRef = useRef<Map<number, RTCPeerConnection>>(
    new Map(),
  );

  const [localStream, setLocalStream] =
    useState<MediaStream | null>(null);

  const [remoteStreams, setRemoteStreams] =
    useState<RemoteStream[]>([]);

  useEffect(() => {
    let active = true;

    async function start() {
      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true,
          video: true,
        });

      if (!active) {
        stream.getTracks().forEach((track) => track.stop());
        return;
      }

      localStreamRef.current = stream;
      setLocalStream(stream);

      const protocol =
        window.location.protocol === "https:"
          ? "wss"
          : "ws";

      const host = window.location.host;

      const socket = new WebSocket(
        `${protocol}://${host}/ws/meetings/${meetingCode}?token=${token}`,
      );

      socketRef.current = socket;

      socket.onmessage = async (event) => {
        const message: SignalMessage =
          JSON.parse(event.data);

        await handleMessage(message);
      };

      socket.onclose = () => {
        console.log("WebSocket closed");
      };
    }

    async function handleMessage(
      message: SignalMessage,
    ) {
      if (message.type === "connected") {
        const participants =
          message.participants ?? [];

        for (const participantId of participants) {
          if (participantId !== message.participant_id) {
            await createOffer(participantId);
          }
        }

        return;
      }

      if (message.type === "participant_joined") {
        const participantId =
          message.participant_id;

        if (participantId) {
          await createOffer(participantId);
        }

        return;
      }

      if (message.type === "offer") {
        await handleOffer(
          message.from!,
          message.data,
        );

        return;
      }

      if (message.type === "answer") {
        const peer =
          peersRef.current.get(message.from!);

        if (!peer) {
          return;
        }

        await peer.setRemoteDescription(
          new RTCSessionDescription(message.data),
        );

        return;
      }

      if (message.type === "ice_candidate") {
        const peer =
          peersRef.current.get(message.from!);

        if (!peer) {
          return;
        }

        await peer.addIceCandidate(
          new RTCIceCandidate(message.data),
        );

        return;
      }

      if (message.type === "participant_left") {
        removePeer(message.participant_id!);
      }
    }

    async function createPeer(
      participantId: number,
    ) {
      const existing =
        peersRef.current.get(participantId);

      if (existing) {
        return existing;
      }

      const peer =
        new RTCPeerConnection({
          iceServers: [
            {
              urls: "stun:stun.l.google.com:19302",
            },
          ],
        });

      peersRef.current.set(
        participantId,
        peer,
      );

      const stream =
        localStreamRef.current;

      if (stream) {
        stream.getTracks().forEach((track) => {
          peer.addTrack(track, stream);
        });
      }

      peer.ontrack = (event) => {
        const stream = event.streams[0];

        if (!stream) {
          return;
        }

        setRemoteStreams((current) => {
          const existing = current.find(
            (item) =>
              item.participantId === participantId,
          );

          if (existing) {
            return current.map((item) =>
              item.participantId === participantId
                ? {
                    ...item,
                    stream,
                  }
                : item,
            );
          }

          return [
            ...current,
            {
              participantId,
              stream,
            },
          ];
        });
      };

      peer.onicecandidate = (event) => {
        if (!event.candidate) {
          return;
        }

        socketRef.current?.send(
          JSON.stringify({
            type: "ice_candidate",
            to: participantId,
            data: event.candidate,
          }),
        );
      };

      return peer;
    }

    async function createOffer(
      participantId: number,
    ) {
      const peer =
        await createPeer(participantId);

      const offer =
        await peer.createOffer();

      await peer.setLocalDescription(
        offer,
      );

      socketRef.current?.send(
        JSON.stringify({
          type: "offer",
          to: participantId,
          data: offer,
        }),
      );
    }

    async function handleOffer(
      participantId: number,
      offer: RTCSessionDescriptionInit,
    ) {
      const peer =
        await createPeer(participantId);

      await peer.setRemoteDescription(
        new RTCSessionDescription(offer),
      );

      const answer =
        await peer.createAnswer();

      await peer.setLocalDescription(
        answer,
      );

      socketRef.current?.send(
        JSON.stringify({
          type: "answer",
          to: participantId,
          data: answer,
        }),
      );
    }

    function removePeer(
      participantId: number,
    ) {
      const peer =
        peersRef.current.get(participantId);

      if (peer) {
        peer.close();
      }

      peersRef.current.delete(
        participantId,
      );

      setRemoteStreams((current) =>
        current.filter(
          (item) =>
            item.participantId !== participantId,
        ),
      );
    }

    start();

    return () => {
      active = false;

      socketRef.current?.close();

      peersRef.current.forEach((peer) => {
        peer.close();
      });

      peersRef.current.clear();

      localStreamRef.current
        ?.getTracks()
        .forEach((track) => track.stop());
    };
  }, [meetingCode, token]);

  return {
    localStream,
    remoteStreams,
  };
}